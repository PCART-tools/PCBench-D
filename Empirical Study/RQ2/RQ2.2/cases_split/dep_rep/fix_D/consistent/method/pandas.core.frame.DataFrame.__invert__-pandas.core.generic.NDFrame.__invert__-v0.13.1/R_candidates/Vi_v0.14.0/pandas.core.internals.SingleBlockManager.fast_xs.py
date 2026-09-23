    def fast_xs(self, loc):
        """
        fast path for getting a cross-section
        return a view of the data
        """
        return self._block.values[loc]
