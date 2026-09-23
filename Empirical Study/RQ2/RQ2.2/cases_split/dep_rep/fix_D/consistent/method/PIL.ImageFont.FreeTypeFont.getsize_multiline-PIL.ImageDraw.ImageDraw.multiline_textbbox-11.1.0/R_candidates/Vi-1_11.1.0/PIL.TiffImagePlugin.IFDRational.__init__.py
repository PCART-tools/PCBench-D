    def __init__(
        self, value: float | Fraction | IFDRational, denominator: int = 1
    ) -> None:
        """
        :param value: either an integer numerator, a
        float/rational/other number, or an IFDRational
        :param denominator: Optional integer denominator
        """
        self._val: Fraction | float
        if isinstance(value, IFDRational):
            self._numerator = value.numerator
            self._denominator = value.denominator
            self._val = value._val
            return

        if isinstance(value, Fraction):
            self._numerator = value.numerator
            self._denominator = value.denominator
        else:
            if TYPE_CHECKING:
                self._numerator = cast(IntegralLike, value)
            else:
                self._numerator = value
            self._denominator = denominator

        if denominator == 0:
            self._val = float("nan")
        elif denominator == 1:
            self._val = Fraction(value)
        elif int(value) == value:
            self._val = Fraction(int(value), denominator)
        else:
            self._val = Fraction(value / denominator)
