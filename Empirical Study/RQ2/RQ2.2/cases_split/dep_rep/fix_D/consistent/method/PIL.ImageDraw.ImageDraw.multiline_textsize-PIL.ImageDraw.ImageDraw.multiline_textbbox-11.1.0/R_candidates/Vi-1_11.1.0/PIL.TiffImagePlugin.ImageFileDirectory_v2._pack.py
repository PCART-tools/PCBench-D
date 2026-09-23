    def _pack(self, fmt: str, *values: Any) -> bytes:
        return struct.pack(self._endian + fmt, *values)
