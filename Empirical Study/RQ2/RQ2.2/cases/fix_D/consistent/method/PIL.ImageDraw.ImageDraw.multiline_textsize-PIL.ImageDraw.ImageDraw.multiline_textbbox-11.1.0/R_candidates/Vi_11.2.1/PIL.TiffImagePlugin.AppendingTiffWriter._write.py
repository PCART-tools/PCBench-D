    def _write(self, value: int, field_size: int) -> None:
        bytes_written = self.f.write(
            struct.pack(self.endian + self._fmt(field_size), value)
        )
        self._verify_bytes_written(bytes_written, field_size)
