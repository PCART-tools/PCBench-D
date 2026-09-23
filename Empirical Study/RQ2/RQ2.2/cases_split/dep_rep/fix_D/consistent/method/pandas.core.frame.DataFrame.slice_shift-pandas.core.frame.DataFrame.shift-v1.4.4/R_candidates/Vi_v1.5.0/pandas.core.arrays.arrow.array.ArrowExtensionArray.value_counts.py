    def value_counts(self, dropna: bool = True) -> Series:
        """
        Return a Series containing counts of each unique value.

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

        vc = self._data.value_counts()

        values = vc.field(0)
        counts = vc.field(1)
        if dropna and self._data.null_count > 0:
            mask = values.is_valid()
            values = values.filter(mask)
            counts = counts.filter(mask)

        # No missing values so we can adhere to the interface and return a numpy array.
        counts = np.array(counts)

        index = Index(type(self)(values))

        return Series(counts, index=index).astype("Int64")
