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
        nv.validate_argsort(args, kwargs)

        if self._step > 0:
            return np.arange(len(self))
        else:
            return np.arange(len(self) - 1, -1, -1)
