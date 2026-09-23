    def _apply_meta(self, rawarr):
        if not isinstance(rawarr, PeriodIndex):
            rawarr = PeriodIndex._from_ordinals(rawarr, freq=self.freq,
                                                name=self.name)
        return rawarr
