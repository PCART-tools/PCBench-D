    def equals(self, other):
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
            except:
                return False

        if not is_dtype_equal(self.dtype, other.dtype):
            # have different timezone
            return False

        # ToDo: Remove this when PeriodDtype is added
        elif isinstance(self, ABCPeriodIndex):
            if not isinstance(other, ABCPeriodIndex):
                return False
            if self.freq != other.freq:
                return False

        return np.array_equal(self.asi8, other.asi8)
