    def xs(self, key, axis=0, copy=False):
        """
        Returns a row (cross-section) from the SparseDataFrame as a Series
        object.

        Parameters
        ----------
        key : some index contained in the index

        Returns
        -------
        xs : Series
        """
        if axis == 1:
            data = self[key]
            return data

        i = self.index.get_loc(key)
        data = self.take([i]).get_values()[0]
        return Series(data, index=self.columns)
