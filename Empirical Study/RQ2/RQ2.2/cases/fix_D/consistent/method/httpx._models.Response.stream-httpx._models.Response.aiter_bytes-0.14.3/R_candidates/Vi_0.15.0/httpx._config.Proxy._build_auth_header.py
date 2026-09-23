    def _build_auth_header(self, username: str, password: str) -> str:
        userpass = (username.encode("utf-8"), password.encode("utf-8"))
        token = b64encode(b":".join(userpass)).decode()
        return f"Basic {token}"
