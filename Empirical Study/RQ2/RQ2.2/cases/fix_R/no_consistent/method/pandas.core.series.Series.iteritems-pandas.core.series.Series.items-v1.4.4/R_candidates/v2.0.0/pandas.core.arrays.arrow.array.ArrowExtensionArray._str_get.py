    def _str_get(self, i: int):
        lengths = pc.utf8_length(self._data)
        if i >= 0:
            out_of_bounds = pc.greater_equal(i, lengths)
            start = i
            stop = i + 1
            step = 1
        else:
            out_of_bounds = pc.greater(-i, lengths)
            start = i
            stop = i - 1
            step = -1
        not_out_of_bounds = pc.invert(out_of_bounds.fill_null(True))
        selected = pc.utf8_slice_codeunits(
            self._data, start=start, stop=stop, step=step
        )
        result = pa.array([None] * self._data.length(), type=self._data.type)
        result = pc.if_else(not_out_of_bounds, selected, result)
        return type(self)(result)
