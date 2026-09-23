    @property
    def raw(self) -> RawURL:
        """
        The URL in the raw representation used by the low level
        transport API. For example, see `httpcore`.

        Provides the (scheme, host, port, target) for the outgoing request.
        """
        return (
            self.scheme.encode("ascii"),
            self.host.encode("ascii"),
            self.port,
            self.raw_path,
        )
