    def __mul__(self, other):
        other = lib.item_from_zerodim(other)

        if isinstance(other, (ABCDataFrame, ABCSeries, ABCIndexClass)):
            return NotImplemented

        if is_scalar(other):
            # numpy will accept float and int, raise TypeError for others
            result = self._data * other
            freq = None
            if self.freq is not None and not isna(other):
                freq = self.freq * other
            return type(self)(result, freq=freq)

        if not hasattr(other, "dtype"):
            # list, tuple
            other = np.array(other)
        if len(other) != len(self) and not is_timedelta64_dtype(other):
            # Exclude timedelta64 here so we correctly raise TypeError
            #  for that instead of ValueError
            raise ValueError("Cannot multiply with unequal lengths")

        if is_object_dtype(other.dtype):
            # this multiplication will succeed only if all elements of other
            #  are int or float scalars, so we will end up with
            #  timedelta64[ns]-dtyped result
            result = [self[n] * other[n] for n in range(len(self))]
            result = np.array(result)
            return type(self)(result)

        # numpy will accept float or int dtype, raise TypeError for others
        result = self._data * other
        return type(self)(result)
