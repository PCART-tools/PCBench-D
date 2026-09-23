    def ravel(self, order='C'):
        """
        Return the flattened underlying data as an ndarray

        See also
        --------
        numpy.ndarray.ravel
        """
        return self._values.ravel(order=order)
