from terminal.init import IntSetting


class Delay(IntSetting):
    key = "delay"
    label = "Пауза между запросами, мс"
    default = 500
    min_value = 0
    max_value = 10000
    step = 100
