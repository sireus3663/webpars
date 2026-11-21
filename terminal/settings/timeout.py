from terminal.init import IntSetting


class Timeout(IntSetting):
    key = "timeout"
    label = "Таймаут запроса, сек"
    default = 10
    min_value = 1
    max_value = 120
    step = 1
