    def argsort(self, *args, **kwargs):
        """
        return an ndarray indexer of the underlying data

        See also
        --------
        numpy.ndarray.argsort
        """
        result = self.asi8
        if result is None:
            result = np.array(self)
        return result.argsort(*args, **kwargs)
