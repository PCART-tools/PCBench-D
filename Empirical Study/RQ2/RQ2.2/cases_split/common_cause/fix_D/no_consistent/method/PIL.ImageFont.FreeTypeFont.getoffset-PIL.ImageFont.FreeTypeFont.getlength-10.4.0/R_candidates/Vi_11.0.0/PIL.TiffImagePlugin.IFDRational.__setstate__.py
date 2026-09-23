    def __setstate__(self, state: list[float | Fraction | IntegralLike]) -> None:
        IFDRational.__init__(self, 0)
        _val, _numerator, _denominator = state
        assert isinstance(_val, (float, Fraction))
        self._val = _val
        if TYPE_CHECKING:
            self._numerator = cast(IntegralLike, _numerator)
        else:
            self._numerator = _numerator
        assert isinstance(_denominator, int)
        self._denominator = _denominator
