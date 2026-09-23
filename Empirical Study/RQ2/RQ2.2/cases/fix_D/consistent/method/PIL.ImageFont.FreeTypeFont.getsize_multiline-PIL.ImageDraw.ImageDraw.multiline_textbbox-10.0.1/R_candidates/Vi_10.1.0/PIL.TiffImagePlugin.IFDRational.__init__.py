    def __init__(self, value, denominator=1):
        """
        :param value: either an integer numerator, a
        float/rational/other number, or an IFDRational
        :param denominator: Optional integer denominator
        """
        if isinstance(value, IFDRational):
            self._numerator = value.numerator
            self._denominator = value.denominator
            self._val = value._val
            return

        if isinstance(value, Fraction):
            self._numerator = value.numerator
            self._denominator = value.denominator
        else:
            self._numerator = value
            self._denominator = denominator

        if denominator == 0:
            self._val = float("nan")
        elif denominator == 1:
            self._val = Fraction(value)
        else:
            self._val = Fraction(value, denominator)
