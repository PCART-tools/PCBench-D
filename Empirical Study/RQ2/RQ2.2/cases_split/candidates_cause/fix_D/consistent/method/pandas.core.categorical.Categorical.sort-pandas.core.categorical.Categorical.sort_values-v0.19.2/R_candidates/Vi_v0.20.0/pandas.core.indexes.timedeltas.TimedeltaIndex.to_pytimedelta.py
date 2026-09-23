    def to_pytimedelta(self):
        """
        Return TimedeltaIndex as object ndarray of datetime.timedelta objects

        Returns
        -------
        datetimes : ndarray
        """
        return libts.ints_to_pytimedelta(self.asi8)
