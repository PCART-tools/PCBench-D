    def ravel(self, order="C"):
        """
        Return an ndarray of the flattened values of the underlying data.

        Returns
        -------
        numpy.ndarray
            Flattened array.

        See Also
        --------
        numpy.ndarray.ravel
        """
        return self._ndarray_values.ravel(order=order)
