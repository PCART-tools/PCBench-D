    @cache_readonly
    def _resolution(self):
        return libresolution.resolution(self.asi8, self.tz)
