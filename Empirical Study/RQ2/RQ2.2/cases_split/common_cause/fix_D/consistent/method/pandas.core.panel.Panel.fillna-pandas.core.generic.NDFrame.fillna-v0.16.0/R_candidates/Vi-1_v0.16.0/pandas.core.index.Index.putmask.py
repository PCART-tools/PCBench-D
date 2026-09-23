    def putmask(self, mask, value):
        """
        return a new Index of the values set with the mask

        See also
        --------
        numpy.ndarray.putmask
        """
        values = self.values.copy()
        np.putmask(values, mask, value)
        return self._shallow_copy(values)
