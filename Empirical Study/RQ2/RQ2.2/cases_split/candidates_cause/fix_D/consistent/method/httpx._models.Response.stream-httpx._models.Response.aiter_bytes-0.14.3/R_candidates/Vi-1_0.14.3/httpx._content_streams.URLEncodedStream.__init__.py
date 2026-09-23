    def __init__(self, data: dict) -> None:
        self.body = urlencode(data, doseq=True).encode("utf-8")
