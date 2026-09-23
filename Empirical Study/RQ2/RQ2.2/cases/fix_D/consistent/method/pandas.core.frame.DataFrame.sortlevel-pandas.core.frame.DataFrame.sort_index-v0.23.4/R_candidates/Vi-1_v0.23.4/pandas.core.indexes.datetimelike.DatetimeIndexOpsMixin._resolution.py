    @cache_readonly
    def _resolution(self):
        return frequencies.Resolution.get_reso_from_freq(self.freqstr)
