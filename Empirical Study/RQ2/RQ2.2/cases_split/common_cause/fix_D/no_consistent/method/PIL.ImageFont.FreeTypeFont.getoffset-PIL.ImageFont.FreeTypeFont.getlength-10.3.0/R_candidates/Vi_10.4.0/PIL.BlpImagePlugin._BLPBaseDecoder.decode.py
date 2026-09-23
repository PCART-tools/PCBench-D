    def decode(self, buffer: bytes) -> tuple[int, int]:
        try:
            self._read_blp_header()
            self._load()
        except struct.error as e:
            msg = "Truncated BLP file"
            raise OSError(msg) from e
        return -1, 0
