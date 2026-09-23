    def splity(self, *args):
        """
        e.g., ``bbox.splitx(f1, f2, ...)``

        Returns a list of new :class:`Bbox` objects formed by
        splitting the original one with horizontal lines at fractional
        positions *f1*, *f2*, ...
        """
        yf = [0] + list(args) + [1]
        x0, y0, x1, y1 = self.extents
        h = y1 - y0
        return [Bbox([[x0, y0 + yf0 * h], [x1, y0 + yf1 * h]])
                for yf0, yf1 in zip(yf[:-1], yf[1:])]
