from terminal.init import IntSetting


class MaxPages(IntSetting):
    key = "max_pages"
    label = "Максимум страниц"
    default = 50
    min_value = 1
    max_value = 5000
    step = 10
