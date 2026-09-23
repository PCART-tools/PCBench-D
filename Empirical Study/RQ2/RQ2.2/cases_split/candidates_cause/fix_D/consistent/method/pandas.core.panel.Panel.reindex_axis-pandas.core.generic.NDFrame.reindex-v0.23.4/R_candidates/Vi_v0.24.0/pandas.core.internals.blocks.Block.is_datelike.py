    @property
    def is_datelike(self):
        """ return True if I am a non-datelike """
        return self.is_datetime or self.is_timedelta
