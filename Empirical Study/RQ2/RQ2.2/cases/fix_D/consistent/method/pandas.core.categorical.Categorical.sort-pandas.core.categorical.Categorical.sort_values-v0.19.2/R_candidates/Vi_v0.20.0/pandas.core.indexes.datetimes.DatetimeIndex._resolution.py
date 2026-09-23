    @cache_readonly
    def _resolution(self):
        return libperiod.resolution(self.asi8, self.tz)
