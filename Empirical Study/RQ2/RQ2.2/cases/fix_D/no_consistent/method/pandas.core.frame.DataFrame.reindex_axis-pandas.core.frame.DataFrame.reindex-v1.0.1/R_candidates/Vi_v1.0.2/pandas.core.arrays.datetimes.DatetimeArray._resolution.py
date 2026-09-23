    @property  # NB: override with cache_readonly in immutable subclasses
    def _resolution(self):
        return libresolution.resolution(self.asi8, self.tz)
