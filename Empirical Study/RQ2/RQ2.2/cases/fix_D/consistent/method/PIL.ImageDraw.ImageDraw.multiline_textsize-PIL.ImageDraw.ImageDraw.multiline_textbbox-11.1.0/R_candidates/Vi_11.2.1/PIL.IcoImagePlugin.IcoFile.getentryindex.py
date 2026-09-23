    def getentryindex(self, size: tuple[int, int], bpp: int | bool = False) -> int:
        for i, h in enumerate(self.entry):
            if size == h.dim and (bpp is False or bpp == h.color_depth):
                return i
        return 0
