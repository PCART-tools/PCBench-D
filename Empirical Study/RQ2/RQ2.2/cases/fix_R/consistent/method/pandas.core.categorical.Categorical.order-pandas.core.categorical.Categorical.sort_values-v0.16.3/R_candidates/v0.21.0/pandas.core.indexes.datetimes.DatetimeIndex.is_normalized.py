    @cache_readonly
    def is_normalized(self):
        """
        Returns True if all of the dates are at midnight ("no time")
        """
        return libts.dates_normalized(self.asi8, self.tz)
