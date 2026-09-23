    def _ixs(self, i, axis=0):
        """
        Return the i-th value or values in the SparseSeries by location

        Parameters
        ----------
        i : int, slice, or sequence of integers

        Returns
        -------
        value : scalar (int) or Series (slice, sequence)
        """
        label = self.index[i]
        if isinstance(label, Index):
            return self.take(i, axis=axis)
        else:
            return self._get_val_at(i)
