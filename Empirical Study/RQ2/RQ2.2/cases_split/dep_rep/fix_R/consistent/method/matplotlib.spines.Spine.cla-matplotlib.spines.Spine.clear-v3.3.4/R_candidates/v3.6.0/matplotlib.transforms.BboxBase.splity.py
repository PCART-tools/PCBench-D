    def splity(self, *args):
        """
        Return a list of new `Bbox` objects formed by splitting the original
        one with horizontal lines at fractional positions given by *args*.
        """
        yf = [0, *args, 1]
        x0, y0, x1, y1 = self.extents
        h = y1 - y0
        return [Bbox([[x0, y0 + yf0 * h], [x1, y0 + yf1 * h]])
                for yf0, yf1 in zip(yf[:-1], yf[1:])]
