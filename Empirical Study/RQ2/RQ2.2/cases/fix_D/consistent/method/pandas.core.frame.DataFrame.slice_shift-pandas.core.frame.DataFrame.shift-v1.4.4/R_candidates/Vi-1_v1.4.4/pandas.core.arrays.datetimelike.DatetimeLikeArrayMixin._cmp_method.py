    def _cmp_method(self, other, op):
        if self.ndim > 1 and getattr(other, "shape", None) == self.shape:
            # TODO: handle 2D-like listlikes
            return op(self.ravel(), other.ravel()).reshape(self.shape)

        try:
            other = self._validate_comparison_value(other)
        except InvalidComparison:
            return invalid_comparison(self, other, op)

        dtype = getattr(other, "dtype", None)
        if is_object_dtype(dtype):
            # We have to use comp_method_OBJECT_ARRAY instead of numpy
            #  comparison otherwise it would fail to raise when
            #  comparing tz-aware and tz-naive
            with np.errstate(all="ignore"):
                result = ops.comp_method_OBJECT_ARRAY(
                    op, np.asarray(self.astype(object)), other
                )
            return result

        other_vals = self._unbox(other)
        # GH#37462 comparison on i8 values is almost 2x faster than M8/m8
        result = op(self._ndarray.view("i8"), other_vals.view("i8"))

        o_mask = isna(other)
        mask = self._isnan | o_mask
        if mask.any():
            nat_result = op is operator.ne
            np.putmask(result, mask, nat_result)

        return result
