    def read_fields(self, field_format: str) -> tuple[int | bytes, ...]:
        size = struct.calcsize(field_format)
        data = self._read_bytes(size)
        return struct.unpack(field_format, data)
