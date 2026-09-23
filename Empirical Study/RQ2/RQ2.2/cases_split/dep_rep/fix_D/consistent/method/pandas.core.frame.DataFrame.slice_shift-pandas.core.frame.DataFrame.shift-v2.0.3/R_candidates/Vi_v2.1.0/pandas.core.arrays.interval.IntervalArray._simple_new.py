    @classmethod
    def _simple_new(
        cls,
        left: IntervalSideT,
        right: IntervalSideT,
        dtype: IntervalDtype,
    ) -> Self:
        result = IntervalMixin.__new__(cls)
        result._left = left
        result._right = right
        result._dtype = dtype

        return result
