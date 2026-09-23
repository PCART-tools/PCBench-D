    def view(self, dtype=None):
        """
        New view on this array with the same data.

        Parameters
        ----------
        dtype : numpy dtype, optional

        Returns
        -------
        ndarray
            With the specified `dtype`.
        """
        return self._data.view(dtype=dtype)
