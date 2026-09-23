    def tz_localize(self, tz, ambiguous='raise'):
        """
        Localize tz-naive DatetimeIndex to given time zone (using
        pytz/dateutil), or remove timezone from tz-aware DatetimeIndex

        Parameters
        ----------
        tz : string, pytz.timezone, dateutil.tz.tzfile or None
            Time zone for time. Corresponding timestamps would be converted to
            time zone of the TimeSeries.
            None will remove timezone holding local time.

        Returns
        -------
        localized : DatetimeIndex

        Notes
        -----
        Not currently implemented for PeriodIndex
        """
        raise NotImplementedError("Not yet implemented for PeriodIndex")
