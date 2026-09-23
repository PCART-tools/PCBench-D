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

        keys, value_counts = algos.value_counts_arraylike(
            self._data, dropna=True, mask=self._mask
        )

        if dropna:
            res = Series(value_counts, index=keys, name="count", copy=False)
            res.index = res.index.astype(self.dtype)
            res = res.astype("Int64")
            return res

        # if we want nans, count the mask
        counts = np.empty(len(value_counts) + 1, dtype="int64")
        counts[:-1] = value_counts
        counts[-1] = self._mask.sum()

        index = Index(keys, dtype=self.dtype).insert(len(keys), self.dtype.na_value)
        index = index.astype(self.dtype)

        mask = np.zeros(len(counts), dtype="bool")
        counts_array = IntegerArray(counts, mask)

        return Series(counts_array, index=index, name="count", copy=False)
