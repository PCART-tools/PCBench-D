    @freq.setter
    def freq(self, value):
        if value is not None:
            value = to_offset(value)
            self._validate_frequency(self, value)

            if self.ndim > 1:
                raise ValueError("Cannot set freq with ndim > 1")

        self._freq = value
