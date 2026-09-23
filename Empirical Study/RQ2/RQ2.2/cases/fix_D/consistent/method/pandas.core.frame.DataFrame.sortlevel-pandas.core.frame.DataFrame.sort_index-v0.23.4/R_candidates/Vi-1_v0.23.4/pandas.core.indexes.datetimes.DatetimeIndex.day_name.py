    def day_name(self, locale=None):
        """
        Return the day names of the DateTimeIndex with specified locale.

        Parameters
        ----------
        locale : string, default None (English locale)
            locale determining the language in which to return the day name

        Returns
        -------
        month_names : Index
            Index of day names

        .. versionadded:: 0.23.0
        """
        values = self.asi8
        if self.tz is not None:
            if self.tz is not utc:
                values = self._local_timestamps()

        result = fields.get_date_name_field(values, 'day_name',
                                            locale=locale)
        result = self._maybe_mask_results(result)
        return Index(result, name=self.name)
