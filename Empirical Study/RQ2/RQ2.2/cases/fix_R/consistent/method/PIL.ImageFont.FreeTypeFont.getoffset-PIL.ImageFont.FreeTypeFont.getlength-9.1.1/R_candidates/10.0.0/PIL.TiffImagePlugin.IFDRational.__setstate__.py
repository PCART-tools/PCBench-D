    def __setstate__(self, state):
        IFDRational.__init__(self, 0)
        _val, _numerator, _denominator = state
        self._val = _val
        self._numerator = _numerator
        self._denominator = _denominator
