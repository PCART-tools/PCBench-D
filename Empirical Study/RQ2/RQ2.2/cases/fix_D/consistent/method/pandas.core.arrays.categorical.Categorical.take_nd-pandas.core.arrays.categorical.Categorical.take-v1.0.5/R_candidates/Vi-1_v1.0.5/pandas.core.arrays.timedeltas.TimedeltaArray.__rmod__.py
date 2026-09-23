    def __rmod__(self, other):
        # Note: This is a naive implementation, can likely be optimized
        if isinstance(other, (ABCSeries, ABCDataFrame, ABCIndexClass)):
            return NotImplemented

        other = lib.item_from_zerodim(other)
        if isinstance(other, (timedelta, np.timedelta64, Tick)):
            other = Timedelta(other)
        return other - (other // self) * self
