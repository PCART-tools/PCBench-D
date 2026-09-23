    def _try_coerce_args(self, other):
        """ provide coercion to our input arguments """

        if isinstance(other, ABCDatetimeIndex):
            # May get a DatetimeIndex here. Unbox it.
            other = other.array

        if isinstance(other, DatetimeArray):
            # hit in pandas/tests/indexing/test_coercion.py
            # ::TestWhereCoercion::test_where_series_datetime64[datetime64tz]
            # when falling back to ObjectBlock.where
            other = other.astype(object)

        return other
