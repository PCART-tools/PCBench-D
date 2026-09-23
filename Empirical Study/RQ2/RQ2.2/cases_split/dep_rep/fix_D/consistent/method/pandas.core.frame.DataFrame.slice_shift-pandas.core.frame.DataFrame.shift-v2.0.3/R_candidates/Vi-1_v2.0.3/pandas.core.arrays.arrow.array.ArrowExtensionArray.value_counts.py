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
        pa_type = self._data.type
        if pa.types.is_duration(pa_type):
            # https://github.com/apache/arrow/issues/15226#issuecomment-1376578323
            data = self._data.cast(pa.int64())
        else:
            data = self._data

        from pandas import (
            Index,
            Series,
        )

        vc = data.value_counts()

        values = vc.field(0)
        counts = vc.field(1)
        if dropna and data.null_count > 0:
            mask = values.is_valid()
            values = values.filter(mask)
            counts = counts.filter(mask)

        if pa.types.is_duration(pa_type):
            values = values.cast(pa_type)

        counts = ArrowExtensionArray(counts)

        index = Index(type(self)(values))

        return Series(counts, index=index, name="count", copy=False)
