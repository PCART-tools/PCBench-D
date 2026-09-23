    def __abs__(self) -> TimedeltaArray:
        # Note: freq is not preserved
        return type(self)(np.abs(self._ndarray))
