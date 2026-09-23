    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def cummax(
        self,
        axis: AxisInt | lib.NoDefault = lib.no_default,
        numeric_only: bool = False,
        **kwargs,
    ) -> NDFrameT:
        """
        Cumulative max for each group.

        Returns
        -------
        Series or DataFrame
        %(see_also)s
        Examples
        --------
        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
        >>> ser = pd.Series([1, 6, 2, 3, 1, 4], index=lst)
        >>> ser
        a    1
        a    6
        a    2
        b    3
        b    1
        b    4
        dtype: int64
        >>> ser.groupby(level=0).cummax()
        a    1
        a    6
        a    6
        b    3
        b    3
        b    4
        dtype: int64

        For DataFrameGroupBy:

        >>> data = [[1, 8, 2], [1, 1, 0], [2, 6, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["cow", "horse", "bull"])
        >>> df
                a   b   c
        cow     1   8   2
        horse   1   1   0
        bull    2   6   9
        >>> df.groupby("a").groups
        {1: ['cow', 'horse'], 2: ['bull']}
        >>> df.groupby("a").cummax()
                b   c
        cow     8   2
        horse   8   2
        bull    6   9
        """
        skipna = kwargs.get("skipna", True)
        if axis is not lib.no_default:
            axis = self.obj._get_axis_number(axis)
            self._deprecate_axis(axis, "cummax")
        else:
            axis = 0

        if axis != 0:
            f = lambda x: np.maximum.accumulate(x, axis)
            obj = self._selected_obj
            if numeric_only:
                obj = obj._get_numeric_data()
            return self._python_apply_general(f, obj, is_transform=True)

        return self._cython_transform(
            "cummax", numeric_only=numeric_only, skipna=skipna
        )
