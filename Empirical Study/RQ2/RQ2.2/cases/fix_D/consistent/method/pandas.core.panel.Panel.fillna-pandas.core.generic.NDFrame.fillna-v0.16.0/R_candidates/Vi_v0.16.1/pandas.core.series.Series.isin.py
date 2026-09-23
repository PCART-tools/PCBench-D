    def isin(self, values):
        """
        Return a boolean :class:`~pandas.Series` showing whether each element
        in the :class:`~pandas.Series` is exactly contained in the passed
        sequence of ``values``.

        Parameters
        ----------
        values : list-like
            The sequence of values to test. Passing in a single string will
            raise a ``TypeError``. Instead, turn a single string into a
            ``list`` of one element.

        Returns
        -------
        isin : Series (bool dtype)

        Raises
        ------
        TypeError
          * If ``values`` is a string

        See Also
        --------
        pandas.DataFrame.isin

        Examples
        --------

        >>> s = pd.Series(list('abc'))
        >>> s.isin(['a', 'c', 'e'])
        0     True
        1    False
        2     True
        dtype: bool

        Passing a single string as ``s.isin('a')`` will raise an error. Use
        a list of one element instead:

        >>> s.isin(['a'])
        0     True
        1    False
        2    False
        dtype: bool

        """
        if not com.is_list_like(values):
            raise TypeError("only list-like objects are allowed to be passed"
                            " to Series.isin(), you passed a "
                            "{0!r}".format(type(values).__name__))

        # may need i8 conversion for proper membership testing
        comps = _values_from_object(self)
        if com.is_datetime64_dtype(self):
            from pandas.tseries.tools import to_datetime
            values = Series(to_datetime(values)).values.view('i8')
            comps = comps.view('i8')
        elif com.is_timedelta64_dtype(self):
            from pandas.tseries.timedeltas import to_timedelta
            values = Series(to_timedelta(values)).values.view('i8')
            comps = comps.view('i8')

        value_set = set(values)
        result = lib.ismember(comps, value_set)
        return self._constructor(result, index=self.index).__finalize__(self)
