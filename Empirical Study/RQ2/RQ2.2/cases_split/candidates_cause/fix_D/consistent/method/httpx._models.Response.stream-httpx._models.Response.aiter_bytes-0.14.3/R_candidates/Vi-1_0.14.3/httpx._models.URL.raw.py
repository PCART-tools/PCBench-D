    @property
    def raw(self) -> typing.Tuple[bytes, bytes, typing.Optional[int], bytes]:
        return (
            self.scheme.encode("ascii"),
            self.host.encode("ascii"),
            self.port,
            self.full_path.encode("ascii"),
        )
