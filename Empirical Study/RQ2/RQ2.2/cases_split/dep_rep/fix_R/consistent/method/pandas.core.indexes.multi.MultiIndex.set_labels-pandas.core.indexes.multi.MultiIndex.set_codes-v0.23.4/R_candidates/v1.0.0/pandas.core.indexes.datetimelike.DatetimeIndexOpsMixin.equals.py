    def equals(self, other) -> bool:
        """
        Determines if two Index objects contain the same elements.
        """
        if self.is_(other):
            return True

        if not isinstance(other, ABCIndexClass):
            return False
        elif not isinstance(other, type(self)):
            try:
                other = type(self)(other)
            except (ValueError, TypeError, OverflowError):
                # e.g.
                #  ValueError -> cannot parse str entry, or OutOfBoundsDatetime
                #  TypeError  -> trying to convert IntervalIndex to DatetimeIndex
                #  OverflowError -> Index([very_large_timedeltas])
                return False

        if not is_dtype_equal(self.dtype, other.dtype):
            # have different timezone
            return False

        return np.array_equal(self.asi8, other.asi8)
