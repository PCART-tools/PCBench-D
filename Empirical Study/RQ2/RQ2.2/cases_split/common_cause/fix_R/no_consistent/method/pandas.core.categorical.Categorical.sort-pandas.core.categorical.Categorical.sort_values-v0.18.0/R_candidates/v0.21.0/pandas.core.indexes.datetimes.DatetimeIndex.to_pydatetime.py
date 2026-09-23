    def to_pydatetime(self):
        """
        Return DatetimeIndex as object ndarray of datetime.datetime objects

        Returns
        -------
        datetimes : ndarray
        """
        return libts.ints_to_pydatetime(self.asi8, tz=self.tz)
