    def ravel(self, order="C"):
        """
        Return the flattened underlying data as an ndarray.

        Returns
        -------
        numpy.ndarray or ndarray-like
            Flattened data of the Series.

        See Also
        --------
        numpy.ndarray.ravel : Return a flattened array.
        """
        return self._values.ravel(order=order)
