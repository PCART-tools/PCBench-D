    def _wrap_setop_result(self, other, result):
        name = get_op_result_name(self, other)
        return self._shallow_copy(result, name=name)
