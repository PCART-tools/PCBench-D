    def limit_rational(self, max_denominator: int) -> tuple[IntegralLike, int]:
        """

        :param max_denominator: Integer, the maximum denominator value
        :returns: Tuple of (numerator, denominator)
        """

        if self.denominator == 0:
            return self.numerator, self.denominator

        assert isinstance(self._val, Fraction)
        f = self._val.limit_denominator(max_denominator)
        return f.numerator, f.denominator
