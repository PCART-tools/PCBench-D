    def _cmp_method(self, other, op):
        pc_func = ARROW_CMP_FUNCS[op.__name__]
        try:
            result = pc_func(self._pa_array, self._box_pa(other))
        except (pa.lib.ArrowNotImplementedError, pa.lib.ArrowInvalid):
            if is_scalar(other):
                mask = isna(self) | isna(other)
                valid = ~mask
                result = np.zeros(len(self), dtype="bool")
                result[valid] = op(np.array(self)[valid], other)
                result = pa.array(result, type=pa.bool_())
                result = pc.if_else(valid, result, None)
            else:
                raise NotImplementedError(
                    f"{op.__name__} not implemented for {type(other)}"
                )
        return ArrowExtensionArray(result)
