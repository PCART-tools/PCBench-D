    def _cmp_method(self, other, op):
        from pandas.arrays import BooleanArray

        pc_func = ARROW_CMP_FUNCS[op.__name__]
        if isinstance(other, ArrowExtensionArray):
            result = pc_func(self._data, other._data)
        elif isinstance(other, (np.ndarray, list)):
            result = pc_func(self._data, other)
        elif is_scalar(other):
            try:
                result = pc_func(self._data, pa.scalar(other))
            except (pa.lib.ArrowNotImplementedError, pa.lib.ArrowInvalid):
                mask = isna(self) | isna(other)
                valid = ~mask
                result = np.zeros(len(self), dtype="bool")
                result[valid] = op(np.array(self)[valid], other)
                return BooleanArray(result, mask)
        else:
            return NotImplementedError(
                f"{op.__name__} not implemented for {type(other)}"
            )

        if pa_version_under2p0:
            result = result.to_pandas().values
        else:
            result = result.to_numpy()
        return BooleanArray._from_sequence(result)
