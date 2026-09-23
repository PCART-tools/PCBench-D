    @classmethod
    def _simple_new(
        cls: type[IntervalArrayT],
        left: IntervalSideT,
        right: IntervalSideT,
        dtype: IntervalDtype,
    ) -> IntervalArrayT:
        result = IntervalMixin.__new__(cls)
        result._left = left
        result._right = right
        result._dtype = dtype

        return result
