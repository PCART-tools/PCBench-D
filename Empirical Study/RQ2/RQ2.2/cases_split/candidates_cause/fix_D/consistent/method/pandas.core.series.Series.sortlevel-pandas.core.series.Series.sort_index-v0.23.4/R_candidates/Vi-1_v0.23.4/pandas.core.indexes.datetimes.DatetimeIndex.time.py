    @property
    def time(self):
        """
        Returns numpy array of datetime.time. The time part of the Timestamps.
        """

        # If the Timestamps have a timezone that is not UTC,
        # convert them into their i8 representation while
        # keeping their timezone and not using UTC
        if (self.tz is not None and self.tz is not utc):
            timestamps = self._local_timestamps()
        else:
            timestamps = self.asi8

        return libts.ints_to_pydatetime(timestamps, box="time")
