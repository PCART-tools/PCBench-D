    def __init__(
        self, username: typing.Union[str, bytes], password: typing.Union[str, bytes]
    ) -> None:
        self._username = to_bytes(username)
        self._password = to_bytes(password)
