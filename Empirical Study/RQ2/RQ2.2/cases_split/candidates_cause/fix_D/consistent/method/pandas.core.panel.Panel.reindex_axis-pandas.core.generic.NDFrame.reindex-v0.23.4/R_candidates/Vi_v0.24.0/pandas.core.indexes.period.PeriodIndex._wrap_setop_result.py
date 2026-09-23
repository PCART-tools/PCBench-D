    def _wrap_setop_result(self, other, result):
        name = get_op_result_name(self, other)
        result = self._apply_meta(result)
        result.name = name
        return result
