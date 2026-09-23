    def _apply_meta(self, rawarr):
        if not isinstance(rawarr, PeriodIndex):
            rawarr = PeriodIndex._simple_new(rawarr, freq=self.freq, name=self.name)
        return rawarr
