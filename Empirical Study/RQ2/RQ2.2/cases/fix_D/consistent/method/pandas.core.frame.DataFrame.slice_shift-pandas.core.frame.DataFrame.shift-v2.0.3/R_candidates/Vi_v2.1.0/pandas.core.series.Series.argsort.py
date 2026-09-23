    def argsort(
        self,
        axis: Axis = 0,
        kind: SortKind = "quicksort",
        order: None = None,
    ) -> Series:
        """
        Return the integer indices that would sort the Series values.

        Override ndarray.argsort. Argsorts the value, omitting NA/null values,
        and places the result in the same locations as the non-NA values.

        Parameters
        ----------
        axis : {0 or 'index'}
            Unused. Parameter needed for compatibility with DataFrame.
        kind : {'mergesort', 'quicksort', 'heapsort', 'stable'}, default 'quicksort'
            Choice of sorting algorithm. See :func:`numpy.sort` for more
            information. 'mergesort' and 'stable' are the only stable algorithms.
        order : None
            Has no effect but is accepted for compatibility with numpy.

        Returns
        -------
        Series[np.intp]
            Positions of values within the sort order with -1 indicating
            nan values.

        See Also
        --------
        numpy.ndarray.argsort : Returns the indices that would sort this array.

        Examples
        --------
        >>> s = pd.Series([3, 2, 1])
        >>> s.argsort()
        0    2
        1    1
        2    0
        dtype: int64
        """
        if axis != -1:
            # GH#54257 We allow -1 here so that np.argsort(series) works
            self._get_axis_number(axis)

        values = self._values
        mask = isna(values)

        if mask.any():
            warnings.warn(
                "The behavior of Series.argsort in the presence of NA values is "
                "deprecated. In a future version, NA values will be ordered "
                "last instead of set to -1.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            result = np.full(len(self), -1, dtype=np.intp)
            notmask = ~mask
            result[notmask] = np.argsort(values[notmask], kind=kind)
        else:
            result = np.argsort(values, kind=kind)

        res = self._constructor(
            result, index=self.index, name=self.name, dtype=np.intp, copy=False
        )
        return res.__finalize__(self, method="argsort")
