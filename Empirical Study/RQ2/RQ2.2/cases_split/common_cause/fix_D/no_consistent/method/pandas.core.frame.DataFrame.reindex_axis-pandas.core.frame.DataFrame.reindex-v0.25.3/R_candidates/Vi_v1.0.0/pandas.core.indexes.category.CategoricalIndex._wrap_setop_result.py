    def _wrap_setop_result(self, other, result):
        name = get_op_result_name(self, other)
        # We use _shallow_copy rather than the Index implementation
        #  (which uses _constructor) in order to preserve dtype.
        return self._shallow_copy(result, name=name)
