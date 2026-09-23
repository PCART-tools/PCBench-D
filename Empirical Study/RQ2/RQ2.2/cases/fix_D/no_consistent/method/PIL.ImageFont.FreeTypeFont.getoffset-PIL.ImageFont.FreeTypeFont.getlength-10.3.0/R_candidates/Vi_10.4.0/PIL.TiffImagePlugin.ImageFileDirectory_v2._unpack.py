    def _unpack(self, fmt, data):
        return struct.unpack(self._endian + fmt, data)
