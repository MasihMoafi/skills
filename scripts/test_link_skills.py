"""Run: python3 test_link_skills.py"""
import contextlib, io, os, tempfile, unittest
from pathlib import Path

from link_skills import main, sync


class LinkSkills(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        self.lib, self.config = root / 'lib', root / 'config'
        self.regs = (root / 'claude', root / 'agents', root / 'codex')
        for d in (self.config, *self.regs):
            d.mkdir()
        for name in ('alpha', 'beta', 'dev'):
            (self.lib / name).mkdir(parents=True)
            (self.lib / name / 'SKILL.md').write_text('---\nname: x\n---\n')
        (self.lib / 'notes').mkdir()  # no SKILL.md: not a skill

    def run_sync(self, apply=True):
        return sync(self.lib, self.regs, self.config, apply)

    def run_main(self, *argv):
        with contextlib.redirect_stdout(io.StringIO()) as printed:
            code = main(list(argv), self.lib, self.regs, self.config)
        return code, printed.getvalue()

    def test_missing_link_is_created(self):
        self.run_sync()
        for reg in self.regs:
            self.assertEqual(os.readlink(reg / 'alpha'), str(self.lib / 'alpha'))
            self.assertFalse((reg / 'dev').exists() or (reg / 'notes').exists())

    def test_link_elsewhere_is_replaced(self):
        (self.regs[0] / 'alpha').symlink_to(self.lib / 'beta')
        self.run_sync()
        self.assertEqual(os.readlink(self.regs[0] / 'alpha'), str(self.lib / 'alpha'))

    def test_dangling_link_is_pruned(self):
        (self.regs[1] / 'gone').symlink_to(self.lib / 'gone')
        self.run_sync()
        self.assertFalse((self.regs[1] / 'gone').is_symlink())

    def test_link_to_folder_without_skill_md_is_pruned(self):
        (self.regs[0] / 'notes').symlink_to(self.lib / 'notes')
        self.run_sync()
        self.assertFalse((self.regs[0] / 'notes').is_symlink())
        self.assertTrue((self.lib / 'notes').is_dir())  # only the link goes

    def test_real_directory_is_left_and_reported(self):
        (self.regs[2] / 'alpha').mkdir()           # a real folder where a library link belongs
        (self.regs[2] / 'synced').mkdir()          # a real folder without SKILL.md
        (self.regs[2] / 'third').mkdir()           # a third-party skill
        (self.regs[2] / 'third' / 'SKILL.md').write_text('x')
        out = '\n'.join(self.run_sync())
        self.assertIn(f'conflict {self.regs[2] / "alpha"}', out)
        self.assertIn(f'conflict {self.regs[2] / "synced"}', out)
        self.assertNotIn('third', out)
        for name in ('alpha', 'synced', 'third'):
            self.assertFalse((self.regs[2] / name).is_symlink())

    def test_config_mirror_gains_and_loses_entries(self):
        (self.config / 'old').symlink_to(self.regs[0] / 'old')
        (self.regs[0] / 'third').mkdir()
        (self.regs[0] / 'third' / 'SKILL.md').write_text('x')
        self.run_sync()
        self.assertEqual(sorted(p.name for p in self.config.iterdir()), ['alpha', 'beta', 'third'])
        self.assertEqual(os.readlink(self.config / 'third'), str(self.regs[0] / 'third'))

    def test_check_changes_nothing_and_sets_exit_code(self):
        (self.regs[1] / 'gone').symlink_to(self.lib / 'gone')
        code, out = self.run_main('--check')
        self.assertEqual(code, 1)
        self.assertIn(f'missing {self.regs[0] / "alpha"}', out)
        self.assertIn(f'dangling {self.regs[1] / "gone"}', out)
        self.assertFalse((self.regs[0] / 'alpha').is_symlink())
        self.assertTrue((self.regs[1] / 'gone').is_symlink())
        self.assertEqual(self.run_main()[0], 0)
        self.assertEqual(self.run_main('--check'), (0, 'skills: ok\n'))


if __name__ == '__main__':
    unittest.main()
