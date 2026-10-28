#!/usr/bin/env python3
"""Use a desktop Electron app (Elpis desktop, ChatGPT, Claude) the way its user does, through the app's
Chromium DevTools port: see its window, read what is on it, click, type and press keys.

  appctl.py launch <app>           start the app with its debug port and wait until it answers
  appctl.py windows <app>          list its windows
  appctl.py shot <app> [png]       screenshot of the front window; prints the PNG path
  appctl.py see <app>              what the user sees, as text (roles, names, values)
  appctl.py click <app> <target>   role:button=Send | text=Settings | label=Search | css=... | xy=120,340
                                   (= matches a whole name, ~= part of one: text~=Sett)
  appctl.py hover|rclick <app> <target>   hover over, or right-click, a target as for click
  appctl.py type <app> <text>      type into the focused field
  appctl.py key <app> <key>        press a key: Enter, Escape, Control+K, ...
  appctl.py eval <app> <js>        run JavaScript in the window and print the result

Add --window N to pick another window from `windows`. The app keeps running between commands.
Claude has no debug port: it runs as an X11 window and takes launch, shot, click xy=, type and key.
"""
import base64, json, os, subprocess, sys, time, urllib.request
from pathlib import Path

os.environ["NO_PROXY"] = os.environ["no_proxy"] = "127.0.0.1,localhost"
APPS = {
    "elpis": {
        "port": int(os.environ.get("APPCTL_ELPIS_PORT", "9336")),
        "cmd": [os.environ.get("APPCTL_ELPIS", str(Path.home() / "Desktop/p/Elpis-wt-continuity/apps/elpis-desktop/desktop/launch.sh"))],
    },
    # Its in-app browser tabs are pages too; `main` picks the app's own window.
    "chatgpt": {"port": 9334, "main": "app://-/index.html", "cmd": ["/usr/lib/chatgpt/ChatGPT", "--proxy-server=http://127.0.0.1:10808"]},
    # Claude refuses to start with a debug port; as an X11 window it is seen and driven by pixels.
    "claude": {"x11": "Claude", "cmd": ["/usr/lib/claude-desktop/claude-desktop", "--ozone-platform=x11"]},
}
OUT = Path("/tmp/appctl")


def debug_port_ready(port):
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        return json.load(opener.open(f"http://127.0.0.1:{port}/json/version", timeout=1))
    except OSError:
        return None


def x11_window(app):
    """The app's largest visible X11 window: (id, x, y, width, height)."""
    def geometry(window):
        out = subprocess.run(["xdotool", "getwindowgeometry", "--shell", window], capture_output=True, text=True).stdout
        g = dict(line.split("=", 1) for line in out.split())
        return window, int(g["X"]), int(g["Y"]), int(g["WIDTH"]), int(g["HEIGHT"])
    found = subprocess.run(["xdotool", "search", "--onlyvisible", "--name", APPS[app]["x11"]],
                           capture_output=True, text=True).stdout.split()
    if not found:
        sys.exit(f"{app} has no visible X11 window; run: appctl.py launch {app}")
    return max((geometry(w) for w in found), key=lambda g: g[3] * g[4])


def x11_command(app, command, args):
    """Pixels only: screenshots, and clicks at window coordinates of those screenshots."""
    if command == "launch":
        OUT.mkdir(exist_ok=True)
        log = open(OUT / f"{app}.log", "ab")
        subprocess.Popen(APPS[app]["cmd"], stdout=log, stderr=log, stdin=subprocess.DEVNULL, start_new_session=True)
        for _ in range(60):
            if subprocess.run(["xdotool", "search", "--onlyvisible", "--name", APPS[app]["x11"]], capture_output=True).stdout:
                return print(f"{app} is up as an X11 window")
            time.sleep(1)
        sys.exit(f"{app} showed no X11 window; if it was already open, close it and launch again")
    window, x, y, width, height = x11_window(app)
    if command == "shot":
        from PIL import Image
        from Xlib import X, display
        OUT.mkdir(exist_ok=True)
        path = Path(args[0]) if args else OUT / f"{app}-{time.strftime('%H%M%S')}.png"
        # Under Wayland only the window's own image can be read, not the screen's.
        raw = display.Display().create_resource_object("window", int(window)).get_image(
            0, 0, width, height, X.ZPixmap, 0xFFFFFFFF)
        Image.frombytes("RGB", (width, height), raw.data, "raw", "BGRX").save(path)
        print(path)
    elif command == "click" and args and args[0].startswith("xy="):
        cx, cy = args[0][3:].split(",")
        subprocess.run(["xdotool", "mousemove", "--window", window, cx, cy, "click", "1"], check=True)
        print("clicked")
    elif command == "type":
        subprocess.run(["xdotool", "type", "--delay", "15", "--", " ".join(args)], check=True)
        print("typed")
    elif command == "key":
        subprocess.run(["xdotool", "key", {"Enter": "Return"}.get(args[0], args[0])], check=True)
        print("pressed")
    else:
        sys.exit(f"{app} is driven by pixels: use launch, shot, click xy=X,Y (screenshot coordinates), type, key")


def launch(app):
    port = APPS[app]["port"]
    if debug_port_ready(port):
        return print(f"{app} already answers on port {port}")
    OUT.mkdir(exist_ok=True)
    log = open(OUT / f"{app}.log", "ab")
    subprocess.Popen(APPS[app]["cmd"] + [f"--remote-debugging-port={port}"], stdout=log, stderr=log,
                     stdin=subprocess.DEVNULL, start_new_session=True)
    for _ in range(240):
        if debug_port_ready(port):
            return print(f"{app} is up on port {port}")
        time.sleep(0.5)
    sys.exit(f"{app} did not open its debug port; see {OUT / (app + '.log')}")


def windows(browser):
    pages = [page for context in browser.contexts for page in context.pages]
    return [page for page in pages if not page.url.startswith("devtools://")]


def front_window(browser, index, main=None):
    pages = windows(browser)
    if main and index is None:
        pages = [p for p in pages if p.url == main] or pages
    if not pages:
        sys.exit("the app has no window")
    if index is not None:
        return pages[index]
    # The main window is the largest visible one; apps also keep small overlays (ChatGPT's pet).
    visible = [p for p in pages if p.evaluate("document.visibilityState") == "visible"]
    return max(visible or pages, key=lambda p: p.evaluate("innerWidth * innerHeight"))


def locate(page, target):
    # `=` matches a whole name and `~=` part of one.
    if target.startswith("role:"):
        role, _, name = target[len("role:"):].partition("=")
        exact = not role.endswith("~")
        return page.get_by_role(role.rstrip("~"), name=name or None, exact=exact).first
    kind, _, value = target.partition("=")
    exact = not kind.endswith("~")
    kind = kind.rstrip("~")
    if kind == "text":
        return page.get_by_text(value, exact=exact).first
    if kind == "label":
        return page.get_by_label(value, exact=exact).first
    if kind == "css":
        return page.locator(value).first
    sys.exit(f"unknown target {target!r}; use role:<role>=<name>, text=, label=, css= or xy=")


def main(argv):
    index = None
    if "--window" in argv:
        at = argv.index("--window")
        index = int(argv[at + 1])
        del argv[at:at + 2]
    if len(argv) < 2 or argv[1] not in APPS:
        sys.exit(__doc__)
    command, app, args = argv[0], argv[1], argv[2:]
    if "x11" in APPS[app]:
        return x11_command(app, command, args)
    if command == "launch":
        return launch(app)
    if not debug_port_ready(APPS[app]["port"]):
        sys.exit(f"{app} is not running with its debug port; run: appctl.py launch {app}")
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        # Disconnecting at exit leaves the app running.
        browser = playwright.chromium.connect_over_cdp(f"http://127.0.0.1:{APPS[app]['port']}")
        if command == "windows":
            for i, page in enumerate(windows(browser)):
                print(i, page.title(), page.url, page.evaluate("document.visibilityState"))
            return
        page = front_window(browser, index, APPS[app].get("main"))
        if command == "shot":
            OUT.mkdir(exist_ok=True)
            path = Path(args[0]) if args else OUT / f"{app}-{time.strftime('%H%M%S')}.png"
            # Straight from the window: Playwright's page.screenshot cuts the right and bottom edges at fractional
            # scales (1.37 here) because it sizes the shot from a viewport it guesses.
            data = page.context.new_cdp_session(page).send("Page.captureScreenshot", {"format": "png"})["data"]
            path.write_bytes(base64.b64decode(data))
            print(path)
        elif command == "see":
            print(page.locator("body").aria_snapshot())
        elif command == "click":
            if args[0].startswith("xy="):
                x, y = (float(v) for v in args[0][3:].split(","))
                page.mouse.click(x, y)
            else:
                try:
                    locate(page, args[0]).click(timeout=5000)
                except Exception as error:  # Playwright's timeout: say what was not found.
                    sys.exit(f"could not click {args[0]!r}: {str(error).splitlines()[0]}")
            print("clicked")
        elif command in ("hover", "rclick"):
            try:
                target = locate(page, args[0])
                target.hover(timeout=5000) if command == "hover" else target.click(button="right", timeout=5000)
            except Exception as error:
                sys.exit(f"could not {command} {args[0]!r}: {str(error).splitlines()[0]}")
            print("done")
        elif command == "type":
            page.keyboard.type(" ".join(args))
            print("typed")
        elif command == "key":
            page.keyboard.press(args[0])
            print("pressed")
        elif command == "eval":
            print(json.dumps(page.evaluate(" ".join(args)), ensure_ascii=False, indent=1))
        else:
            sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
