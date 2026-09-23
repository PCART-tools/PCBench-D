    def _slice(self, slicer):
        """ return a slice of my values """
        if isinstance(slicer, tuple):
            col, loc = slicer
            if not com.is_null_slice(col) and col != 0:
                raise IndexError(f"{self} only contains one item")
            return self.values[loc]
        return self.values[slicer]
