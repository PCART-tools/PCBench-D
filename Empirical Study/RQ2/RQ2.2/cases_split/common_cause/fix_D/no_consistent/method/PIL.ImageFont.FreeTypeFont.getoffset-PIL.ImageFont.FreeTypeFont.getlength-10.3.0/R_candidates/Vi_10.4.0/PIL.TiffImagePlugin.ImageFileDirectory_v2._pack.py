    def _pack(self, fmt, *values):
        return struct.pack(self._endian + fmt, *values)
