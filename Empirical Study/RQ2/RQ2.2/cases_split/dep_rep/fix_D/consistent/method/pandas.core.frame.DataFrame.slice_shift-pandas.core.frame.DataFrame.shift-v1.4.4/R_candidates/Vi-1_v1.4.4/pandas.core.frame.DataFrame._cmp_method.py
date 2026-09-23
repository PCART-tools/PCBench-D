    def _cmp_method(self, other, op):
        axis = 1  # only relevant for Series other case

        self, other = ops.align_method_FRAME(self, other, axis, flex=False, level=None)

        # See GH#4537 for discussion of scalar op behavior
        new_data = self._dispatch_frame_op(other, op, axis=axis)
        return self._construct_result(new_data)
