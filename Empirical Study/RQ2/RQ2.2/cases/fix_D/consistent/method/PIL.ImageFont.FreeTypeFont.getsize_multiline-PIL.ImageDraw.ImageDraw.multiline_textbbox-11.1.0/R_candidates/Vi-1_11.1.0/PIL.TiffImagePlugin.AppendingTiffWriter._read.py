    def _read(self, field_size: int) -> int:
        (value,) = struct.unpack(
            self.endian + self._fmt(field_size), self.f.read(field_size)
        )
        return value
