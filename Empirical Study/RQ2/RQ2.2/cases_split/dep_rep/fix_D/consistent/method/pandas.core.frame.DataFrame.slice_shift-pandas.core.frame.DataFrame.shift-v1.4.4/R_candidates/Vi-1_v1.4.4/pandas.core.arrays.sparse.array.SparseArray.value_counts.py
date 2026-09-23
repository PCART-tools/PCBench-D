    def value_counts(self, dropna: bool = True) -> Series:
        """
        Returns a Series containing counts of unique values.

        Parameters
        ----------
        dropna : bool, default True
            Don't include counts of NaN, even if NaN is in sp_values.

        Returns
        -------
        counts : Series
        """
        from pandas import (
            Index,
            Series,
        )

        keys, counts = algos.value_counts_arraylike(self.sp_values, dropna=dropna)
        fcounts = self.sp_index.ngaps
        if fcounts > 0 and (not self._null_fill_value or not dropna):
            mask = isna(keys) if self._null_fill_value else keys == self.fill_value
            if mask.any():
                counts[mask] += fcounts
            else:
                keys = np.insert(keys, 0, self.fill_value)
                counts = np.insert(counts, 0, fcounts)

        if not isinstance(keys, ABCIndex):
            keys = Index(keys)
        return Series(counts, index=keys)
