    def _read_bgra(
        self, palette: list[tuple[int, int, int, int]], alpha: bool
    ) -> bytearray:
        data = bytearray()
        _data = BytesIO(self._safe_read(self._lengths[0]))
        while True:
            try:
                (offset,) = struct.unpack("<B", _data.read(1))
            except struct.error:
                break
            b, g, r, a = palette[offset]
            d: tuple[int, ...] = (r, g, b)
            if alpha:
                d += (a,)
            data.extend(d)
        return data
