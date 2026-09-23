    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def cumsum(
        self, axis: Axis | lib.NoDefault = lib.no_default, *args, **kwargs
    ) -> NDFrameT:
        """
        Cumulative sum for each group.

        Returns
        -------
        Series or DataFrame
        %(see_also)s
        Examples
        --------
        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'b']
        >>> ser = pd.Series([6, 2, 0], index=lst)
        >>> ser
        a    6
        a    2
        b    0
        dtype: int64
        >>> ser.groupby(level=0).cumsum()
        a    6
        a    8
        b    0
        dtype: int64

        For DataFrameGroupBy:

        >>> data = [[1, 8, 2], [1, 2, 5], [2, 6, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["fox", "gorilla", "lion"])
        >>> df
                  a   b   c
        fox       1   8   2
        gorilla   1   2   5
        lion      2   6   9
        >>> df.groupby("a").groups
        {1: ['fox', 'gorilla'], 2: ['lion']}
        >>> df.groupby("a").cumsum()
                  b   c
        fox       8   2
        gorilla  10   7
        lion      6   9
        """
        nv.validate_groupby_func("cumsum", args, kwargs, ["numeric_only", "skipna"])
        if axis is not lib.no_default:
            axis = self.obj._get_axis_number(axis)
            self._deprecate_axis(axis, "cumsum")
        else:
            axis = 0

        if axis != 0:
            f = lambda x: x.cumsum(axis=axis, **kwargs)
            return self._python_apply_general(f, self._selected_obj, is_transform=True)

        return self._cython_transform("cumsum", **kwargs)
