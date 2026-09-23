    @final
    def _wrap_setop_result(self, other: Index, result) -> Index:
        name = get_op_result_name(self, other)
        if isinstance(result, Index):
            if result.name != name:
                result = result.rename(name)
        else:
            result = self._shallow_copy(result, name=name)

        if type(self) is Index and self.dtype != _dtype_obj:
            # i.e. ExtensionArray-backed
            # TODO(ExtensionIndex): revert this astype; it is a kludge to make
            #  it possible to split ExtensionEngine from ExtensionIndex PR.
            return result.astype(self.dtype, copy=False)
        return result
