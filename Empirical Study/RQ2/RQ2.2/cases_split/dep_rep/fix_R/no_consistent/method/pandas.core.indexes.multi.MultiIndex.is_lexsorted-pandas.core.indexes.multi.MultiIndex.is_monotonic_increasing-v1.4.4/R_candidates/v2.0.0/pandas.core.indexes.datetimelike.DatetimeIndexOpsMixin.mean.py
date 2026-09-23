    @doc(DatetimeLikeArrayMixin.mean)
    def mean(self, *, skipna: bool = True, axis: int | None = 0):
        return self._data.mean(skipna=skipna, axis=axis)
