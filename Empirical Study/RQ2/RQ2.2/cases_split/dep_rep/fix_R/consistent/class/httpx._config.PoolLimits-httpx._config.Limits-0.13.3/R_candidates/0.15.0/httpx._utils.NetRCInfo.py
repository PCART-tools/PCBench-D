class NetRCInfo:
    def __init__(self, files: typing.Optional[typing.List[str]] = None) -> None:
        if files is None:
            files = [os.getenv("NETRC", ""), "~/.netrc", "~/_netrc"]
        self.netrc_files = files

    @property
    def netrc_info(self) -> typing.Optional[netrc.netrc]:
        if not hasattr(self, "_netrc_info"):
            self._netrc_info = None
            for file_path in self.netrc_files:
                expanded_path = Path(file_path).expanduser()
                try:
                    if expanded_path.is_file():
                        self._netrc_info = netrc.netrc(str(expanded_path))
                        break
                except (netrc.NetrcParseError, IOError):  # pragma: nocover
                    # Issue while reading the netrc file, ignore...
                    pass
        return self._netrc_info

    def get_credentials(self, host: str) -> typing.Optional[typing.Tuple[str, str]]:
        if self.netrc_info is None:
            return None

        auth_info = self.netrc_info.authenticators(host)
        if auth_info is None or auth_info[2] is None:
            return None
        return (auth_info[0], auth_info[2])
