    @property  # NB: override with cache_readonly in immutable subclasses
    def _timezone(self):
        """
        Comparable timezone both for pytz / dateutil
        """
        return timezones.get_timezone(self.tzinfo)
