    def month_name(self, locale=None):
        """
        Return the month names of the DateTimeIndex with specified locale.

        .. versionadded:: 0.23.0

        Parameters
        ----------
        locale : str, optional
            Locale determining the language in which to return the month name.
            Default is English locale.

        Returns
        -------
        Index
            Index of month names.

        Examples
        --------
        >>> idx = pd.date_range(start='2018-01', freq='M', periods=3)
        >>> idx
        DatetimeIndex(['2018-01-31', '2018-02-28', '2018-03-31'],
                      dtype='datetime64[ns]', freq='M')
        >>> idx.month_name()
        Index(['January', 'February', 'March'], dtype='object')
        """
        if self.tz is not None and not timezones.is_utc(self.tz):
            values = self._local_timestamps()
        else:
            values = self.asi8

        result = fields.get_date_name_field(values, "month_name", locale=locale)
        result = self._maybe_mask_results(result, fill_value=None)
        return result
