    def _logical_method(self, other, op):
        # For integer types `^`, `|`, `&` are bitwise operators and return
        # integer types. Otherwise these are boolean ops.
        if pa.types.is_integer(self._pa_array.type):
            return self._evaluate_op_method(other, op, ARROW_BIT_WISE_FUNCS)
        else:
            return self._evaluate_op_method(other, op, ARROW_LOGICAL_FUNCS)
