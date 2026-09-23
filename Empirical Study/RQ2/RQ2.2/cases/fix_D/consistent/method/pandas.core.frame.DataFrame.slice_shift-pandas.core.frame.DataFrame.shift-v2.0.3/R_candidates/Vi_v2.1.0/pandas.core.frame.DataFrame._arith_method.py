    def _arith_method(self, other, op):
        if self._should_reindex_frame_op(other, op, 1, None, None):
            return self._arith_method_with_reindex(other, op)

        axis: Literal[1] = 1  # only relevant for Series other case
        other = ops.maybe_prepare_scalar_for_op(other, (self.shape[axis],))

        self, other = self._align_for_op(other, axis, flex=True, level=None)

        with np.errstate(all="ignore"):
            new_data = self._dispatch_frame_op(other, op, axis=axis)
        return self._construct_result(new_data)
