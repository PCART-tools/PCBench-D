    def check_xy(self, xy: tuple[int, int]) -> tuple[int, int]:
        (x, y) = xy
        if not (0 <= x < self.xsize and 0 <= y < self.ysize):
            msg = "pixel location out of range"
            raise ValueError(msg)
        return xy
