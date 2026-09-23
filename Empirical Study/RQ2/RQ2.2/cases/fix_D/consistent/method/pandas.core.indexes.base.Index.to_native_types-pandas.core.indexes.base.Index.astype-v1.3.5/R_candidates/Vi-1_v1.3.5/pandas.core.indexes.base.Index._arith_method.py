    def _arith_method(self, other, op):
        """
        Wrapper used to dispatch arithmetic operations.
        """

        from pandas import Series

        result = op(Series(self), other)
        if isinstance(result, tuple):
            return (Index(result[0]), Index(result[1]))
        return Index(result)
