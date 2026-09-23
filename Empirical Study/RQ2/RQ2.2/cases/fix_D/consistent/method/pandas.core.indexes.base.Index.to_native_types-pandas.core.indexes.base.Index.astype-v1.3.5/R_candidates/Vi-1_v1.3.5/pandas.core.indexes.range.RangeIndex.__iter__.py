    @doc(Int64Index.__iter__)
    def __iter__(self):
        yield from self._range
