    def month_name(self, locale=None):
        """
        Return the month names of the :class:`~pandas.Series` or
        :class:`~pandas.DatetimeIndex` with specified locale.

        Parameters
        ----------
        locale : str, optional
            Locale determining the language in which to return the month name.
            Default is English locale.

        Returns
        -------
        Series or Index
            Series or Index of month names.

        Examples
        --------
        >>> s = pd.Series(pd.date_range(start='2018-01', freq='M', periods=3))
        >>> s
        0   2018-01-31
        1   2018-02-28
        2   2018-03-31
        dtype: datetime64[ns]
        >>> s.dt.month_name()
        0     January
        1    February
        2       March
        dtype: object

        >>> idx = pd.date_range(start='2018-01', freq='M', periods=3)
        >>> idx
        DatetimeIndex(['2018-01-31', '2018-02-28', '2018-03-31'],
                      dtype='datetime64[ns]', freq='M')
        >>> idx.month_name()
        Index(['January', 'February', 'March'], dtype='object')
        """
        values = self._local_timestamps()

        result = fields.get_date_name_field(values, "month_name", locale=locale)
        result = self._maybe_mask_results(result, fill_value=None)
        return result
