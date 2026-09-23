    def __init__(
        self, username: typing.Union[str, bytes], password: typing.Union[str, bytes]
    ):
        self._auth_header = self._build_auth_header(username, password)
