    @final
    def _wrap_setop_result(self, other, result):
        if isinstance(self, (ABCDatetimeIndex, ABCTimedeltaIndex)) and isinstance(
            result, np.ndarray
        ):
            result = type(self._data)._simple_new(result, dtype=self.dtype)
        elif is_categorical_dtype(self.dtype) and isinstance(result, np.ndarray):
            result = Categorical(result, dtype=self.dtype)

        name = get_op_result_name(self, other)
        if isinstance(result, Index):
            if result.name != name:
                return result.rename(name)
            return result
        else:
            return self._shallow_copy(result, name=name)
