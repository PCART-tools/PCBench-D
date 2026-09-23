    def argsort(self, *args, **kwargs) -> np.ndarray:
        """
        Returns the indices that would sort the index and its
        underlying data.

        Returns
        -------
        argsorted : numpy array

        See Also
        --------
        numpy.ndarray.argsort
        """
        nv.validate_argsort(args, kwargs)

        if self._range.step > 0:
            return np.arange(len(self))
        else:
            return np.arange(len(self) - 1, -1, -1)
