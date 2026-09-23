    def value_counts(self, dropna: bool = True) -> Series:
        """
        Returns a Series containing counts of each unique value.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of missing values.

        Returns
        -------
        counts : Series

        See Also
        --------
        Series.value_counts
        """
        from pandas import (
            Index,
            Series,
        )
        from pandas.arrays import IntegerArray

        # compute counts on the data with no nans
        data = self._data[~self._mask]
        value_counts = Index(data).value_counts()

        index = value_counts.index

        # if we want nans, count the mask
        if dropna:
            counts = value_counts._values
        else:
            counts = np.empty(len(value_counts) + 1, dtype="int64")
            counts[:-1] = value_counts
            counts[-1] = self._mask.sum()

            index = index.insert(len(index), self.dtype.na_value)

        index = index.astype(self.dtype)

        mask = np.zeros(len(counts), dtype="bool")
        counts = IntegerArray(counts, mask)

        return Series(counts, index=index)
