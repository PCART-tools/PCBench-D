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
