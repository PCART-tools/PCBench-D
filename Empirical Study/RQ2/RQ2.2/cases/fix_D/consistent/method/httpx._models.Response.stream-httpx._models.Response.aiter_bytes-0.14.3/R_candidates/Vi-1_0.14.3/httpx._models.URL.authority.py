    @property
    def authority(self) -> str:
        port_str = self._uri_reference.port
        default_port_str = {"https": "443", "http": "80"}.get(self.scheme, "")
        if port_str is None or port_str == default_port_str:
            return self._uri_reference.host or ""
        return self._uri_reference.authority or ""
