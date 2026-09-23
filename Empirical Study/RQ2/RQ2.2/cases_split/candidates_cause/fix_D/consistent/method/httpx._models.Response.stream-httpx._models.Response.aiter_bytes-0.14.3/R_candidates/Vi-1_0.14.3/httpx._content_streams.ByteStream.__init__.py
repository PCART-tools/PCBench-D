    def __init__(self, body: typing.Union[str, bytes]) -> None:
        self.body = body.encode("utf-8") if isinstance(body, str) else body
