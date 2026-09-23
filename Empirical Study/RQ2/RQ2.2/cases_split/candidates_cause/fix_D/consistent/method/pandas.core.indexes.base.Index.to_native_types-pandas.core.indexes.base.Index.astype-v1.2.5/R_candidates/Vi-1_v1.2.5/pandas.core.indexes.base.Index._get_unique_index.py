    def _get_unique_index(self, dropna: bool = False):
        """
        Returns an index containing unique values.

        Parameters
        ----------
        dropna : bool, default False
            If True, NaN values are dropped.

        Returns
        -------
        uniques : index
        """
        if self.is_unique and not dropna:
            return self

        if not self.is_unique:
            values = self.unique()
            if not isinstance(self, ABCMultiIndex):
                # extract an array to pass to _shallow_copy
                values = values._data
        else:
            values = self._values

        if dropna and not isinstance(self, ABCMultiIndex):
            # isna not defined for MultiIndex
            if self.hasnans:
                values = values[~isna(values)]

        return self._shallow_copy(values)
