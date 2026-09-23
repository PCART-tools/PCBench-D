    @property  # NB: override with cache_readonly in immutable subclasses
    def _resolution(self):
        return frequencies.Resolution.get_reso_from_freq(self.freqstr)
