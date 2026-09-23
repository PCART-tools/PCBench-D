    def _read_palette(self):
        ret = []
        for i in range(256):
            try:
                b, g, r, a = struct.unpack("<4B", self._safe_read(4))
            except struct.error:
                break
            ret.append((b, g, r, a))
        return ret
