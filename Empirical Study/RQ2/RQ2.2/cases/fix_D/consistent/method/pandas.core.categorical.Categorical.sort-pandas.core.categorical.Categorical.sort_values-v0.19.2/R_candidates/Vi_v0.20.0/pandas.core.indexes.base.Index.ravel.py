    def ravel(self, order='C'):
        """
        return an ndarray of the flattened values of the underlying data

        See also
        --------
        numpy.ndarray.ravel
        """
        return self._values.ravel(order=order)
