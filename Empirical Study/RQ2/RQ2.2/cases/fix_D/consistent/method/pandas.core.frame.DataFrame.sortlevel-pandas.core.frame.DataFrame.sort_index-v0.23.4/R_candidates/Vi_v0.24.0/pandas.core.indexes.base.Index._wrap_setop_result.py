    def _wrap_setop_result(self, other, result):
        return self._constructor(result, name=get_op_result_name(self, other))
