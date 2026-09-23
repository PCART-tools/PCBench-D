    def _scalar_from_string(self, value):
        # type: (str) -> Period
        return Period(value, freq=self.freq)
