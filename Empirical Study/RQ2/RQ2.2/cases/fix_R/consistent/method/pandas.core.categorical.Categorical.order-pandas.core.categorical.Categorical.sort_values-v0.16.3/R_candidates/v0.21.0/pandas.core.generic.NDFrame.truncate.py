    def truncate(self, before=None, after=None, axis=None, copy=True):
        """
        Truncates a sorted DataFrame/Series before and/or after some
        particular index value. If the axis contains only datetime values,
        before/after parameters are converted to datetime values.

        Parameters
        ----------
        before : date, string, int
            Truncate all rows before this index value
        after : date, string, int
            Truncate all rows after this index value
        axis : {0 or 'index', 1 or 'columns'}

            * 0 or 'index': apply truncation to rows
            * 1 or 'columns': apply truncation to columns
            Default is stat axis for given data type (0 for Series and
            DataFrames, 1 for Panels)
        copy : boolean, default is True,
            return a copy of the truncated section

        Returns
        -------
        truncated : type of caller

        Examples
        --------
        >>> df = pd.DataFrame({'A': ['a', 'b', 'c', 'd', 'e'],
        ...                    'B': ['f', 'g', 'h', 'i', 'j'],
        ...                    'C': ['k', 'l', 'm', 'n', 'o']},
        ...                    index=[1, 2, 3, 4, 5])
        >>> df.truncate(before=2, after=4)
           A  B  C
        2  b  g  l
        3  c  h  m
        4  d  i  n
        >>> df = pd.DataFrame({'A': [1, 2, 3, 4, 5],
        ...                    'B': [6, 7, 8, 9, 10],
        ...                    'C': [11, 12, 13, 14, 15]},
        ...                    index=['a', 'b', 'c', 'd', 'e'])
        >>> df.truncate(before='b', after='d')
           A  B   C
        b  2  7  12
        c  3  8  13
        d  4  9  14

        The index values in ``truncate`` can be datetimes or string
        dates. Note that ``truncate`` assumes a 0 value for any unspecified
        date component in a ``DatetimeIndex`` in contrast to slicing which
        returns any partially matching dates.

        >>> dates = pd.date_range('2016-01-01', '2016-02-01', freq='s')
        >>> df = pd.DataFrame(index=dates, data={'A': 1})
        >>> df.truncate('2016-01-05', '2016-01-10').tail()
                             A
        2016-01-09 23:59:56  1
        2016-01-09 23:59:57  1
        2016-01-09 23:59:58  1
        2016-01-09 23:59:59  1
        2016-01-10 00:00:00  1
        >>> df.loc['2016-01-05':'2016-01-10', :].tail()
                             A
        2016-01-10 23:59:55  1
        2016-01-10 23:59:56  1
        2016-01-10 23:59:57  1
        2016-01-10 23:59:58  1
        2016-01-10 23:59:59  1
        """

        if axis is None:
            axis = self._stat_axis_number
        axis = self._get_axis_number(axis)
        ax = self._get_axis(axis)

        # if we have a date index, convert to dates, otherwise
        # treat like a slice
        if ax.is_all_dates:
            from pandas.core.tools.datetimes import to_datetime
            before = to_datetime(before)
            after = to_datetime(after)

        if before is not None and after is not None:
            if before > after:
                raise ValueError('Truncate: %s must be after %s' %
                                 (after, before))

        slicer = [slice(None, None)] * self._AXIS_LEN
        slicer[axis] = slice(before, after)
        result = self.loc[tuple(slicer)]

        if isinstance(ax, MultiIndex):
            setattr(result, self._get_axis_name(axis),
                    ax.truncate(before, after))

        if copy:
            result = result.copy()

        return result
