    @freq.setter
    def freq(self, value):
        if value is not None:
            value = frequencies.to_offset(value)
            self._validate_frequency(self, value)

        self._freq = value
