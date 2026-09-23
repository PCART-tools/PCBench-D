    @property  # NB: override with cache_readonly in immutable subclasses
    def _resolution_obj(self) -> Optional[Resolution]:
        try:
            return Resolution.get_reso_from_freq(self.freqstr)
        except KeyError:
            return None
