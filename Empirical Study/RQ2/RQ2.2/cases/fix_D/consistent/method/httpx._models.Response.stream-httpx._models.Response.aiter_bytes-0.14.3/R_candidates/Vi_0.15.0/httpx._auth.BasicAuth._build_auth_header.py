    def _build_auth_header(
        self, username: typing.Union[str, bytes], password: typing.Union[str, bytes]
    ) -> str:
        userpass = b":".join((to_bytes(username), to_bytes(password)))
        token = b64encode(userpass).decode()
        return f"Basic {token}"
