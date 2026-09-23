    def __getstate__(self):
        return [self._val, self._numerator, self._denominator]
