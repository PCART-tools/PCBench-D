    def _slice(self, slicer):
        """ return a slice of my values """
        if isinstance(slicer, tuple):
            col, loc = slicer
            if not is_null_slice(col) and col != 0:
                raise IndexError("{0} only contains one item".format(self))
            return self.values[loc]
        return self.values[slicer]
