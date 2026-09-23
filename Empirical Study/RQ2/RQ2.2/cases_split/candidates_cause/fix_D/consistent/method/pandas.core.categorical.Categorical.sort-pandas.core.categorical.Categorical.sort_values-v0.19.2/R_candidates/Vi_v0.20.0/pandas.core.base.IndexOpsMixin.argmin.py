    def argmin(self, axis=None):
        """
        return a ndarray of the minimum argument indexer

        See also
        --------
        numpy.ndarray.argmin
        """
        return nanops.nanargmin(self.values)
