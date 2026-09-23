    def _rewriteLast(self, value: int, field_size: int) -> None:
        self.f.seek(-field_size, os.SEEK_CUR)
        bytes_written = self.f.write(
            struct.pack(self.endian + self._fmt(field_size), value)
        )
        self._verify_bytes_written(bytes_written, field_size)
