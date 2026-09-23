    def _get_allsegs_and_allkinds(self):
        """
        Create and return allsegs and allkinds by calling underlying C code.
        """
        allsegs = []
        if self.filled:
            lowers, uppers = self._get_lowers_and_uppers()
            allkinds = []
            for lower, upper in zip(lowers, uppers):
                segs, kinds = self.cppContourGenerator.create_filled_contour(
                    lower, upper)
                allsegs.append([segs])
                allkinds.append([kinds])
        else:
            allkinds = None
            for level in self.levels:
                segs = self.cppContourGenerator.create_contour(level)
                allsegs.append(segs)
        return allsegs, allkinds
