    def _arith_method(self, other, op):
        if ops.should_reindex_frame_op(self, other, op, 1, None, None):
            return ops.frame_arith_method_with_reindex(self, other, op)

        axis: Literal[1] = 1  # only relevant for Series other case
        other = ops.maybe_prepare_scalar_for_op(other, (self.shape[axis],))

        self, other = ops.align_method_FRAME(self, other, axis, flex=True, level=None)

        new_data = self._dispatch_frame_op(other, op, axis=axis)
        return self._construct_result(new_data)
