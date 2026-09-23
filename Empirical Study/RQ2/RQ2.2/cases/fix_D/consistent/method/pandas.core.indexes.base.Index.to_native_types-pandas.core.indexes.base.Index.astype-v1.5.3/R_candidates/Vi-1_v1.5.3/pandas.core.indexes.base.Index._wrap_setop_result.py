    @final
    def _wrap_setop_result(self, other: Index, result) -> Index:
        name = get_op_result_name(self, other)
        if isinstance(result, Index):
            if result.name != name:
                result = result.rename(name)
        else:
            result = self._shallow_copy(result, name=name)
        return result
