    def draft(self, mode, size):
        if len(self.tile) != 1:
            return

        # Protect from second call
        if self.decoderconfig:
            return

        d, e, o, a = self.tile[0]
        scale = 1
        original_size = self.size

        if a[0] == "RGB" and mode in ["L", "YCbCr"]:
            self._mode = mode
            a = mode, ""

        if size:
            scale = min(self.size[0] // size[0], self.size[1] // size[1])
            for s in [8, 4, 2, 1]:
                if scale >= s:
                    break
            e = (
                e[0],
                e[1],
                (e[2] - e[0] + s - 1) // s + e[0],
                (e[3] - e[1] + s - 1) // s + e[1],
            )
            self._size = ((self.size[0] + s - 1) // s, (self.size[1] + s - 1) // s)
            scale = s

        self.tile = [(d, e, o, a)]
        self.decoderconfig = (scale, 0)

        box = (0, 0, original_size[0] / scale, original_size[1] / scale)
        return self.mode, box
