    def combine(self, other, func, fill_value=None, overwrite=True):
        """
        Add two DataFrame objects and do not propagate NaN values, so if for a
        (column, time) one frame is missing a value, it will default to the
        other frame's value (which might be NaN as well)

        Parameters
        ----------
        other : DataFrame
        func : function
            Function that takes two series as inputs and return a Series or a
            scalar
        fill_value : scalar value
        overwrite : boolean, default True
            If True then overwrite values for common keys in the calling frame

        Returns
        -------
        result : DataFrame

        Examples
        --------
        >>> df1 = DataFrame({'A': [0, 0], 'B': [4, 4]})
        >>> df2 = DataFrame({'A': [1, 1], 'B': [3, 3]})
        >>> df1.combine(df2, lambda s1, s2: s1 if s1.sum() < s2.sum() else s2)
           A  B
        0  0  3
        1  0  3

        See Also
        --------
        DataFrame.combine_first : Combine two DataFrame objects and default to
            non-null values in frame calling the method
        """
        other_idxlen = len(other.index)  # save for compare

        this, other = self.align(other, copy=False)
        new_index = this.index

        if other.empty and len(new_index) == len(self.index):
            return self.copy()

        if self.empty and len(other) == other_idxlen:
            return other.copy()

        # sorts if possible
        new_columns = this.columns.union(other.columns)
        do_fill = fill_value is not None

        result = {}
        for col in new_columns:
            series = this[col]
            otherSeries = other[col]

            this_dtype = series.dtype
            other_dtype = otherSeries.dtype

            this_mask = isna(series)
            other_mask = isna(otherSeries)

            # don't overwrite columns unecessarily
            # DO propagate if this column is not in the intersection
            if not overwrite and other_mask.all():
                result[col] = this[col].copy()
                continue

            if do_fill:
                series = series.copy()
                otherSeries = otherSeries.copy()
                series[this_mask] = fill_value
                otherSeries[other_mask] = fill_value

            # if we have different dtypes, possibly promote
            new_dtype = this_dtype
            if not is_dtype_equal(this_dtype, other_dtype):
                new_dtype = find_common_type([this_dtype, other_dtype])
                if not is_dtype_equal(this_dtype, new_dtype):
                    series = series.astype(new_dtype)
                if not is_dtype_equal(other_dtype, new_dtype):
                    otherSeries = otherSeries.astype(new_dtype)

            # see if we need to be represented as i8 (datetimelike)
            # try to keep us at this dtype
            needs_i8_conversion_i = needs_i8_conversion(new_dtype)
            if needs_i8_conversion_i:
                arr = func(series, otherSeries, True)
            else:
                arr = func(series, otherSeries)

            arr = maybe_downcast_to_dtype(arr, this_dtype)

            result[col] = arr

        # convert_objects just in case
        return self._constructor(result, index=new_index,
                                 columns=new_columns)._convert(datetime=True,
                                                               copy=False)
