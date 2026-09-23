    def ravel(self, order='C'):
        """
        return an ndarray of the flattened values of the underlying data

        See also
        --------
        numpy.ndarray.ravel
        """
        return self._ndarray_values.ravel(order=order)
