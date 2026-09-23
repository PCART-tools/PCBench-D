    @final
    def truncate(
        self,
        before=None,
        after=None,
        axis: Axis | None = None,
        copy: bool_t | None = None,
    ) -> Self:
        """
        Truncate a Series or DataFrame before and after some index value.

        This is a useful shorthand for boolean indexing based on index
        values above or below certain thresholds.

        Parameters
        ----------
        before : date, str, int
            Truncate all rows before this index value.
        after : date, str, int
            Truncate all rows after this index value.
        axis : {0 or 'index', 1 or 'columns'}, optional
            Axis to truncate. Truncates the index (rows) by default.
            For `Series` this parameter is unused and defaults to 0.
        copy : bool, default is True,
            Return a copy of the truncated section.

        Returns
        -------
        type of caller
            The truncated Series or DataFrame.

        See Also
        --------
        DataFrame.loc : Select a subset of a DataFrame by label.
        DataFrame.iloc : Select a subset of a DataFrame by position.

        Notes
        -----
        If the index being truncated contains only datetime values,
        `before` and `after` may be specified as strings instead of
        Timestamps.

        Examples
        --------
        >>> df = pd.DataFrame({'A': ['a', 'b', 'c', 'd', 'e'],
        ...                    'B': ['f', 'g', 'h', 'i', 'j'],
        ...                    'C': ['k', 'l', 'm', 'n', 'o']},
        ...                   index=[1, 2, 3, 4, 5])
        >>> df
           A  B  C
        1  a  f  k
        2  b  g  l
        3  c  h  m
        4  d  i  n
        5  e  j  o

        >>> df.truncate(before=2, after=4)
           A  B  C
        2  b  g  l
        3  c  h  m
        4  d  i  n

        The columns of a DataFrame can be truncated.

        >>> df.truncate(before="A", after="B", axis="columns")
           A  B
        1  a  f
        2  b  g
        3  c  h
        4  d  i
        5  e  j

        For Series, only rows can be truncated.

        >>> df['A'].truncate(before=2, after=4)
        2    b
        3    c
        4    d
        Name: A, dtype: object

        The index values in ``truncate`` can be datetimes or string
        dates.

        >>> dates = pd.date_range('2016-01-01', '2016-02-01', freq='s')
        >>> df = pd.DataFrame(index=dates, data={'A': 1})
        >>> df.tail()
                             A
        2016-01-31 23:59:56  1
        2016-01-31 23:59:57  1
        2016-01-31 23:59:58  1
        2016-01-31 23:59:59  1
        2016-02-01 00:00:00  1

        >>> df.truncate(before=pd.Timestamp('2016-01-05'),
        ...             after=pd.Timestamp('2016-01-10')).tail()
                             A
        2016-01-09 23:59:56  1
        2016-01-09 23:59:57  1
        2016-01-09 23:59:58  1
        2016-01-09 23:59:59  1
        2016-01-10 00:00:00  1

        Because the index is a DatetimeIndex containing only dates, we can
        specify `before` and `after` as strings. They will be coerced to
        Timestamps before truncation.

        >>> df.truncate('2016-01-05', '2016-01-10').tail()
                             A
        2016-01-09 23:59:56  1
        2016-01-09 23:59:57  1
        2016-01-09 23:59:58  1
        2016-01-09 23:59:59  1
        2016-01-10 00:00:00  1

        Note that ``truncate`` assumes a 0 value for any unspecified time
        component (midnight). This differs from partial string slicing, which
        returns any partially matching dates.

        >>> df.loc['2016-01-05':'2016-01-10', :].tail()
                             A
        2016-01-10 23:59:55  1
        2016-01-10 23:59:56  1
        2016-01-10 23:59:57  1
        2016-01-10 23:59:58  1
        2016-01-10 23:59:59  1
        """
        if axis is None:
            axis = 0
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        # GH 17935
        # Check that index is sorted
        if not ax.is_monotonic_increasing and not ax.is_monotonic_decreasing:
            raise ValueError("truncate requires a sorted index")

        # if we have a date index, convert to dates, otherwise
        # treat like a slice
        if ax._is_all_dates:
            from pandas.core.tools.datetimes import to_datetime

            before = to_datetime(before)
            after = to_datetime(after)

        if before is not None and after is not None and before > after:
            raise ValueError(f"Truncate: {after} must be after {before}")

        if len(ax) > 1 and ax.is_monotonic_decreasing and ax.nunique() > 1:
            before, after = after, before

        slicer = [slice(None, None)] * self._AXIS_LEN
        slicer[axis] = slice(before, after)
        result = self.loc[tuple(slicer)]

        if isinstance(ax, MultiIndex):
            setattr(result, self._get_axis_name(axis), ax.truncate(before, after))

        result = result.copy(deep=copy and not using_copy_on_write())

        return result
