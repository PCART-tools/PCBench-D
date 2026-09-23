    def ravel(self, order='C'):
        """
        Return the flattened underlying data as an ndarray

        See also
        --------
        numpy.ndarray.ravel
        """
        return self.values.ravel(order=order)
