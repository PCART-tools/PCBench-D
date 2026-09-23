    def _combine_const(self, other, func):
        assert lib.is_scalar(other) or np.ndim(other) == 0
        return ops.dispatch_to_series(self, other, func)
