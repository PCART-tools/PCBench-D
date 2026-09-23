    @final
    def get_group(self, name, obj=None) -> DataFrame | Series:
        """
        Construct DataFrame from group with provided name.

        Parameters
        ----------
        name : object
            The name of the group to get as a DataFrame.
        obj : DataFrame, default None
            The DataFrame to take the DataFrame out of.  If
            it is None, the object groupby was called on will
            be used.

            .. deprecated:: 2.1.0
                The obj is deprecated and will be removed in a future version.
                Do ``df.iloc[gb.indices.get(name)]``
                instead of ``gb.get_group(name, obj=df)``.

        Returns
        -------
        same type as obj

        Examples
        --------

        For SeriesGroupBy:

        >>> lst = ['a', 'a', 'b']
        >>> ser = pd.Series([1, 2, 3], index=lst)
        >>> ser
        a    1
        a    2
        b    3
        dtype: int64
        >>> ser.groupby(level=0).get_group("a")
        a    1
        a    2
        dtype: int64

        For DataFrameGroupBy:

        >>> data = [[1, 2, 3], [1, 5, 6], [7, 8, 9]]
        >>> df = pd.DataFrame(data, columns=["a", "b", "c"],
        ...                   index=["owl", "toucan", "eagle"])
        >>> df
                a  b  c
        owl     1  2  3
        toucan  1  5  6
        eagle   7  8  9
        >>> df.groupby(by=["a"]).get_group(1)
                a  b  c
        owl     1  2  3
        toucan  1  5  6

        For Resampler:

        >>> ser = pd.Series([1, 2, 3, 4], index=pd.DatetimeIndex(
        ...                 ['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15']))
        >>> ser
        2023-01-01    1
        2023-01-15    2
        2023-02-01    3
        2023-02-15    4
        dtype: int64
        >>> ser.resample('MS').get_group('2023-01-01')
        2023-01-01    1
        2023-01-15    2
        dtype: int64
        """
        inds = self._get_index(name)
        if not len(inds):
            raise KeyError(name)

        if obj is None:
            return self._selected_obj.iloc[inds]
        else:
            warnings.warn(
                "obj is deprecated and will be removed in a future version. "
                "Do ``df.iloc[gb.indices.get(name)]`` "
                "instead of ``gb.get_group(name, obj=df)``.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            return obj._take_with_is_copy(inds, axis=self.axis)
