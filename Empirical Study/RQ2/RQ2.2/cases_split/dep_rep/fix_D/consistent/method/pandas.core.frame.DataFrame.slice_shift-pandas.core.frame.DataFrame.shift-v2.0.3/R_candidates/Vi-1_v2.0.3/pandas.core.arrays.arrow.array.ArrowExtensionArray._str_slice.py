    def _str_slice(
        self, start: int | None = None, stop: int | None = None, step: int | None = None
    ):
        if start is None:
            start = 0
        if step is None:
            step = 1
        return type(self)(
            pc.utf8_slice_codeunits(self._data, start=start, stop=stop, step=step)
        )
