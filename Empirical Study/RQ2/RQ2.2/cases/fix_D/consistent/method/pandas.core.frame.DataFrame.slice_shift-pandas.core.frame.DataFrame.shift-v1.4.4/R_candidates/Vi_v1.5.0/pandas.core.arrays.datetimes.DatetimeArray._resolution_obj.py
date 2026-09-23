    @property  # NB: override with cache_readonly in immutable subclasses
    def _resolution_obj(self) -> Resolution:
        return get_resolution(self.asi8, self.tz, reso=self._reso)
