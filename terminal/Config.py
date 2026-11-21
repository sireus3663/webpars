class Config:
    def __init__(self):
        self.url = ""
        self.max_pages = 50
        self.max_depth = 2
        self.delay = 500
        self.timeout = 10
        self.respect_robots = True

    def __str__(self):
        robots = "да" if self.respect_robots else "нет"
        return (
            f"URL: {self.url}\n"
            f"Максимум страниц: {self.max_pages}\n"
            f"Максимум глубины: {self.max_depth}\n"
            f"Пауза между запросами, мс: {self.delay}\n"
            f"Таймаут запроса, сек: {self.timeout}\n"
            f"Уважать robots.txt: {robots}"
        )