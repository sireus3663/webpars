from terminal.init import IntSetting


class MaxDepth(IntSetting):
    key = "max_depth"
    label = "Максимум глубины"
    default = 2
    min_value = 0
    max_value = 20
    step = 1
