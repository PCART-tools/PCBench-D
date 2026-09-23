    def _arith_method(self, other, op):
        self, other = self._align_for_op(other)
        return base.IndexOpsMixin._arith_method(self, other, op)
