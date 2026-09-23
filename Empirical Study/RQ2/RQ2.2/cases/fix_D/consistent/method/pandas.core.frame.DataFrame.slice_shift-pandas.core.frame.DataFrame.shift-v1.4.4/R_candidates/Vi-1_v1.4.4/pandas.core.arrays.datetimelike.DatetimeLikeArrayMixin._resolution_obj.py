    @property  # NB: override with cache_readonly in immutable subclasses
    def _resolution_obj(self) -> Resolution | None:
        freqstr = self.freqstr
        if freqstr is None:
            return None
        try:
            return Resolution.get_reso_from_freq(freqstr)
        except KeyError:
            return None
