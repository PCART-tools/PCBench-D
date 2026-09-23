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

        if dropna:
            keys, counts = algos.value_counts_arraylike(
                self._data, dropna=True, mask=self._mask
            )
            res = Series(counts, index=keys)
            res.index = res.index.astype(self.dtype)
            res = res.astype("Int64")
            return res

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
        counts_array = IntegerArray(counts, mask)

        return Series(counts_array, index=index)
