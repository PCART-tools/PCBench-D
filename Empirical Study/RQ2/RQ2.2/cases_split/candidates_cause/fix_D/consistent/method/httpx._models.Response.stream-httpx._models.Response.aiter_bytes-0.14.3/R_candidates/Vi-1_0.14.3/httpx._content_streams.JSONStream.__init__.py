    def __init__(self, json: typing.Any) -> None:
        self.body = json_dumps(json).encode("utf-8")
