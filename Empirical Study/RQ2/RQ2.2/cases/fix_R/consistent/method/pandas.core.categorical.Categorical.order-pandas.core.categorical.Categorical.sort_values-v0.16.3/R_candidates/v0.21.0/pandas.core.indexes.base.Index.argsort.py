    def argsort(self, *args, **kwargs):
        """
        Returns the indices that would sort the index and its
        underlying data.

        Returns
        -------
        argsorted : numpy array

        See also
        --------
        numpy.ndarray.argsort
        """
        result = self.asi8
        if result is None:
            result = np.array(self)
        return result.argsort(*args, **kwargs)
