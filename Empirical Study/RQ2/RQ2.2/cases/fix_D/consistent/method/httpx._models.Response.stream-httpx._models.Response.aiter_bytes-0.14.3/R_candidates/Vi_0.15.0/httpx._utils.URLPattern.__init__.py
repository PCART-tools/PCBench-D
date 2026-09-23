    def __init__(self, pattern: str) -> None:
        from ._models import URL

        if pattern and ":" not in pattern:
            warn_deprecated(
                f"Proxy keys should use proper URL forms rather "
                f"than plain scheme strings. "
                f'Instead of "{pattern}", use "{pattern}://"'
            )
            pattern += "://"

        url = URL(pattern)
        self.pattern = pattern
        self.scheme = "" if url.scheme == "all" else url.scheme
        self.host = "" if url.host == "*" else url.host
        self.port = url.port
        if not url.host or url.host == "*":
            self.host_regex: typing.Optional[typing.Pattern[str]] = None
        else:
            if url.host.startswith("*."):
                # *.example.com should match "www.example.com", but not "example.com"
                domain = re.escape(url.host[2:])
                self.host_regex = re.compile(f"^.+\\.{domain}$")
            elif url.host.startswith("*"):
                # *example.com should match "www.example.com" and "example.com"
                domain = re.escape(url.host[1:])
                self.host_regex = re.compile(f"^(.+\\.)?{domain}$")
            else:
                # example.com should match "example.com" but not "www.example.com"
                domain = re.escape(url.host)
                self.host_regex = re.compile(f"^{domain}$")
