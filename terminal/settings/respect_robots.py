from terminal.init import BoolSetting


class RespectRobots(BoolSetting):
    key = "respect_robots"
    label = "Уважать robots.txt"
    default = True
