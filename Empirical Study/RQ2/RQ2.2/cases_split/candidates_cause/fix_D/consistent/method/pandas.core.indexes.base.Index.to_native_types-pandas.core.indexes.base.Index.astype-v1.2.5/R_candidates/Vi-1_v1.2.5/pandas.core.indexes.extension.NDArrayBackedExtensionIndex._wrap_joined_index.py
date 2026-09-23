    def _wrap_joined_index(self: _T, joined: np.ndarray, other: _T) -> _T:
        name = get_op_result_name(self, other)
        arr = self._data._from_backing_data(joined)
        return type(self)._simple_new(arr, name=name)
