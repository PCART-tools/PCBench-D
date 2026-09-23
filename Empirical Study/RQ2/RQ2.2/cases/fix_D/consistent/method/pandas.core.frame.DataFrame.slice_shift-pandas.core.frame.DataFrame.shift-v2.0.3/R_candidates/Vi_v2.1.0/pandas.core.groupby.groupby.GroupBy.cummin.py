    @final
    @Substitution(name="groupby")
    @Substitution(see_also=_common_see_also)
    def cummin(
        self,
        axis: AxisInt | lib.NoDefault = lib.no_default,
        numeric_only: bool = False,
        **kwargs,
    ) -> NDFrameT:
        """
        Cumulative min for each group.

        Returns
        -------
        Series or DataFrame
        %(see_also)s
        Examples
        --------
        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'a', 'b', 'b', 'b']
        >>> ser = pd.Series([1, 6, 2, 3, 0, 4], index=lst)
        >>> ser
        a    1
        a    6
        a    2
        b    3
        b    0
        b    4
        dtype: int64
        >>> ser.groupby(level=0).cummin()
        a    1
        a    1
        a    1
        b    3
        b    0
        b    0
        dtype: int64

        For DataFrameGroupBy:

        >>> data = [[1, 0, 2], [1, 1, 5], [6, 6, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["snake", "rabbit", "turtle"])
        >>> df
                a   b   c
        snake   1   0   2
        rabbit  1   1   5
        turtle  6   6   9
        >>> df.groupby("a").groups
        {1: ['snake', 'rabbit'], 6: ['turtle']}
        >>> df.groupby("a").cummin()
                b   c
        snake   0   2
        rabbit  0   2
        turtle  6   9
        """
        skipna = kwargs.get("skipna", True)
        if axis is not lib.no_default:
            axis = self.obj._get_axis_number(axis)
            self._deprecate_axis(axis, "cummin")
        else:
            axis = 0

        if axis != 0:
            f = lambda x: np.minimum.accumulate(x, axis)
            obj = self._selected_obj
            if numeric_only:
                obj = obj._get_numeric_data()
            return self._python_apply_general(f, obj, is_transform=True)

        return self._cython_transform(
            "cummin", numeric_only=numeric_only, skipna=skipna
        )
