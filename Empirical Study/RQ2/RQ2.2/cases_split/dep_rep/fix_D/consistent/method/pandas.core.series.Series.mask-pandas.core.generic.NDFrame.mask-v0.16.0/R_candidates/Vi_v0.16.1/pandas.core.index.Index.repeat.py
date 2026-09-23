    def repeat(self, n):
        """
        return a new Index of the values repeated n times

        See also
        --------
        numpy.ndarray.repeat
        """
        return self._shallow_copy(self.values.repeat(n))
