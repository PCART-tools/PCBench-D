    def _rewriteLast(
        self, value: int, field_size: int, new_field_size: int = 0
    ) -> None:
        self.f.seek(-field_size, os.SEEK_CUR)
        if not new_field_size:
            new_field_size = field_size
        bytes_written = self.f.write(
            struct.pack(self.endian + self._fmt(new_field_size), value)
        )
        self._verify_bytes_written(bytes_written, new_field_size)
