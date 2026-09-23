    def stroke(self):
        """
        Predicate: does the path need to be stroked (its outline drawn)?
        This tests for the various conditions that disable stroking
        the path, in which case it would presumably be filled.
        """
        # _linewidth > 0: in pdf a line of width 0 is drawn at minimum
        #   possible device width, but e.g., agg doesn't draw at all
        return (self._linewidth > 0 and self._alpha > 0 and
                (len(self._rgb) <= 3 or self._rgb[3] != 0.0))
