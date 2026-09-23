    def argmax(self, axis=None):
        """
        return a ndarray of the maximum argument indexer

        See also
        --------
        numpy.ndarray.argmax
        """
        return nanops.nanargmax(self.values)
