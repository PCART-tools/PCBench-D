    def splitx(self, *args):
        """
        e.g., ``bbox.splitx(f1, f2, ...)``

        Returns a list of new :class:`Bbox` objects formed by
        splitting the original one with vertical lines at fractional
        positions *f1*, *f2*, ...
        """
        xf = [0, *args, 1]
        x0, y0, x1, y1 = self.extents
        w = x1 - x0
        return [Bbox([[x0 + xf0 * w, y0], [x0 + xf1 * w, y1]])
                for xf0, xf1 in zip(xf[:-1], xf[1:])]
