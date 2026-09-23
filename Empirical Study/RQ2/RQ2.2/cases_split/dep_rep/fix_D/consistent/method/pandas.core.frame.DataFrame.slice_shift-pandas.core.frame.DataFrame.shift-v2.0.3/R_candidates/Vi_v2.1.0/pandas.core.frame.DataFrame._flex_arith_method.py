    def _flex_arith_method(
        self, other, op, *, axis: Axis = "columns", level=None, fill_value=None
    ):
        axis = self._get_axis_number(axis) if axis is not None else 1

        if self._should_reindex_frame_op(other, op, axis, fill_value, level):
            return self._arith_method_with_reindex(other, op)

        if isinstance(other, Series) and fill_value is not None:
            # TODO: We could allow this in cases where we end up going
            #  through the DataFrame path
            raise NotImplementedError(f"fill_value {fill_value} not supported.")

        other = ops.maybe_prepare_scalar_for_op(other, self.shape)
        self, other = self._align_for_op(other, axis, flex=True, level=level)

        with np.errstate(all="ignore"):
            if isinstance(other, DataFrame):
                # Another DataFrame
                new_data = self._combine_frame(other, op, fill_value)

            elif isinstance(other, Series):
                new_data = self._dispatch_frame_op(other, op, axis=axis)
            else:
                # in this case we always have `np.ndim(other) == 0`
                if fill_value is not None:
                    self = self.fillna(fill_value)

                new_data = self._dispatch_frame_op(other, op)

        return self._construct_result(new_data)
