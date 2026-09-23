    def __getstate__(self) -> list[float | Fraction | IntegralLike]:
        return [self._val, self._numerator, self._denominator]
