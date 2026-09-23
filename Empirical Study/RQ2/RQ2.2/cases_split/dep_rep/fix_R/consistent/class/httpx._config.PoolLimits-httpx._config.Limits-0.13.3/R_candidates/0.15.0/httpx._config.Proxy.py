class Proxy:
    def __init__(
        self, url: URLTypes, *, headers: HeaderTypes = None, mode: str = "DEFAULT"
    ):
        url = URL(url)
        headers = Headers(headers)

        if url.scheme not in ("http", "https"):
            raise ValueError(f"Unknown scheme for proxy URL {url!r}")
        if mode not in ("DEFAULT", "FORWARD_ONLY", "TUNNEL_ONLY"):
            raise ValueError(f"Unknown proxy mode {mode!r}")

        if url.username or url.password:
            headers.setdefault(
                "Proxy-Authorization",
                self._build_auth_header(url.username, url.password),
            )
            # Remove userinfo from the URL authority, e.g.:
            # 'username:password@proxy_host:proxy_port' -> 'proxy_host:proxy_port'
            url = url.copy_with(username=None, password=None)

        self.url = url
        self.headers = headers
        self.mode = mode

    def _build_auth_header(self, username: str, password: str) -> str:
        userpass = (username.encode("utf-8"), password.encode("utf-8"))
        token = b64encode(b":".join(userpass)).decode()
        return f"Basic {token}"

    def __repr__(self) -> str:
        return (
            f"Proxy(url={str(self.url)!r}, "
            f"headers={dict(self.headers)!r}, "
            f"mode={self.mode!r})"
        )
