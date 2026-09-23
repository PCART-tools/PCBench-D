    def _arith_method(self, other, op):
        self, other = ops.align_method_SERIES(self, other)
        return base.IndexOpsMixin._arith_method(self, other, op)
