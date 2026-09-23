    def day_name(self, locale=None):
        """
        Return the day names of the DateTimeIndex with specified locale.

        .. versionadded:: 0.23.0

        Parameters
        ----------
        locale : str, optional
            Locale determining the language in which to return the day name.
            Default is English locale.

        Returns
        -------
        Index
            Index of day names.

        Examples
        --------
        >>> idx = pd.date_range(start='2018-01-01', freq='D', periods=3)
        >>> idx
        DatetimeIndex(['2018-01-01', '2018-01-02', '2018-01-03'],
                      dtype='datetime64[ns]', freq='D')
        >>> idx.day_name()
        Index(['Monday', 'Tuesday', 'Wednesday'], dtype='object')
        """
        if self.tz is not None and not timezones.is_utc(self.tz):
            values = self._local_timestamps()
        else:
            values = self.asi8

        result = fields.get_date_name_field(values, 'day_name',
                                            locale=locale)
        result = self._maybe_mask_results(result, fill_value=None)
        return result
