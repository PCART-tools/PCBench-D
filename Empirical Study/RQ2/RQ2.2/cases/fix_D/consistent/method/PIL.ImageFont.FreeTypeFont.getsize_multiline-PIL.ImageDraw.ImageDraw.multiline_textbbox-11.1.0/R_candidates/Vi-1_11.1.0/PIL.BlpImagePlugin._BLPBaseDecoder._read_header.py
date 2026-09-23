    def _read_header(self) -> None:
        self._offsets = struct.unpack("<16I", self._safe_read(16 * 4))
        self._lengths = struct.unpack("<16I", self._safe_read(16 * 4))
