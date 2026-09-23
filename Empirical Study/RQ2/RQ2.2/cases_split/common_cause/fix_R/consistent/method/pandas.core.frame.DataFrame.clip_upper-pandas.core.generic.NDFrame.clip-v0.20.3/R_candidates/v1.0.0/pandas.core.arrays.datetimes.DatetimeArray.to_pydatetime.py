    def to_pydatetime(self):
        """
        Return Datetime Array/Index as object ndarray of datetime.datetime
        objects.

        Returns
        -------
        datetimes : ndarray
        """
        return tslib.ints_to_pydatetime(self.asi8, tz=self.tz)
