import msvcrt
import os
import sys
from abc import ABC, abstractmethod

from terminal.Config import Config


def load_settings(): #массив параметров
    from terminal.settings.max_pages import MaxPages
    from terminal.settings.max_depth import MaxDepth
    from terminal.settings.delay import Delay
    from terminal.settings.timeout import Timeout
    from terminal.settings.respect_robots import RespectRobots

    return [MaxPages(), MaxDepth(), Delay(), Timeout(), RespectRobots()]


class Setting(ABC):
    key = ""
    label = ""
    default = None

    def __init__(self):
        self.value = self.default

    @abstractmethod
    def render(self): #принт
        ...

    @abstractmethod
    def activate(self): #нажатие
        ...

    def change(self, delta): #переключение
        pass

    def set_text(self, text): #ручной сет
        pass


class BoolSetting(Setting):
    def render(self):
        return "[y]" if self.value else "[n]"

    def activate(self):
        self.value = not self.value

    def change(self, delta):
        self.value = not self.value


class IntSetting(Setting):
    def render(self):
        return str(self.value)

    def activate(self):
        return "text"

    def change(self, delta):
        value = self.value + delta * self.step
        self.value = max(self.min_value, min(self.max_value, value))

    def set_text(self, text):
        try:
            value = int(text)
        except ValueError:
            return
        self.value = max(self.min_value, min(self.max_value, value))




def read_key():
    char = msvcrt.getwch()
    if char in ("\x00", "\xe0"):
        code = msvcrt.getwch()
        return {
            "H": "up",
            "P": "down",
            "K": "left",
            "M": "right",
        }.get(code, "unknown")
    if char == "\r":
        return "enter"
    if char == "\x1b":
        return "esc"
    if char in ("\x08", "\x7f"):
        return "backspace"
    return char


def enable_ansi(): #добавить поддержку mac и линукс
    if os.name == "nt":
        os.system("")


def setup_console(): #смена кодировки для поддержки русского
    if os.name != "nt":
        return
    os.system("chcp 65001 >nul")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass


def hide_cursor():
    sys.stdout.write("\x1b[?25l")
    sys.stdout.flush()


def show_cursor():
    sys.stdout.write("\x1b[?25h")
    sys.stdout.flush()


def clear():
    sys.stdout.write("\x1b[2J\x1b[H")
    sys.stdout.flush()


def render(lines):
    sys.stdout.write("\x1b[H" + "\n".join(lines) + "\x1b[J")
    sys.stdout.flush()


class Terminal:
    def __init__(self):
        self.url = ""
        self.settings = []
        self.selected = 0

    def run(self):
        setup_console()
        self.url = self.ask_url()
        self.settings = load_settings()
        if os.name == "nt" and sys.stdin.isatty():
            self.interactive()

        config = Config()
        config.url = self.url
        for setting in self.settings:
            setattr(config, setting.key, setting.value)
        return config

    def interactive(self):
        if not self.settings:
            return
        enable_ansi()
        hide_cursor()
        try:
            clear()
            self.menu()
        except KeyboardInterrupt:
            pass
        finally:
            show_cursor()
            sys.stdout.write("\n")
            sys.stdout.flush()

    def ask_url(self):
        while True:
            try:
                raw = input("URL сайта: ").strip()
            except EOFError:
                raise SystemExit("\nURL не введён.") from None
            if raw:
                return raw
            print("Ссылка не может быть пустой.")

    def menu(self):
        while True:
            self.draw()
            key = read_key()
            if key == "up":
                self.selected = (self.selected - 1) % len(self.settings)
            elif key == "down":
                self.selected = (self.selected + 1) % len(self.settings)
            elif key == "left":
                self.settings[self.selected].change(-1)
            elif key == "right":
                self.settings[self.selected].change(1)
            elif key == "enter":
                if self.settings[self.selected].activate() == "text":
                    self.edit_int(self.settings[self.selected])
            elif key in ("esc", "eof", "\x03"):
                return

    def draw(self, prompt=None):
        lines = [f"URL: {self.url}", ""]
        for index, setting in enumerate(self.settings):
            marker = ">" if index == self.selected else " "
            row = f"{marker} {setting.render():>6}  {setting.label}"
            if index == self.selected:
                row = f"\x1b[7m{row}\x1b[0m"
            lines.append(row)
        lines.append("")
        lines.append(
            "\x1b[2m↑↓ выбор   ←→ изменить   "
            "Enter ввод/переключить   Esc готово\x1b[0m"
        )
        if prompt is not None:
            lines.append("")
            lines.append(prompt)
        render(lines)

    def edit_int(self, setting):
        buffer = ""
        while True:
            self.draw(f"Число ({setting.min_value}..{setting.max_value}): {buffer}_")
            key = read_key()
            if key == "enter":
                if buffer:
                    setting.set_text(buffer)
                return
            if key in ("esc", "eof", "\x03"):
                return
            if key == "backspace":
                buffer = buffer[:-1]
                continue
            if key == "-" and not buffer and setting.min_value < 0:
                buffer = "-"
                continue
            if key.isdigit():
                buffer += key
