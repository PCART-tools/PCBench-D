    @property
    def timetz(self):
        """
        Returns numpy array of datetime.time also containing timezone
        information. The time part of the Timestamps.
        """
        return tslib.ints_to_pydatetime(self.asi8, self.tz, box="time")
