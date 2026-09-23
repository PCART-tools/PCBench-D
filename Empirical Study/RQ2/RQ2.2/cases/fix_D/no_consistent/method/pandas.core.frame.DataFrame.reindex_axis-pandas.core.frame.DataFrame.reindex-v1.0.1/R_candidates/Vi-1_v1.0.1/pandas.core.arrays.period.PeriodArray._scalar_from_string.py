    def _scalar_from_string(self, value: str) -> Period:
        return Period(value, freq=self.freq)
