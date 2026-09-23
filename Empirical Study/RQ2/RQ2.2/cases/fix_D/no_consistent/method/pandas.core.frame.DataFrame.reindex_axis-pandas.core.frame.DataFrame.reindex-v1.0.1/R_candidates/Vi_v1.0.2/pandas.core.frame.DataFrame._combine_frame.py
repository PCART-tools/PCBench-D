    def _combine_frame(self, other, func, fill_value=None, level=None):
        # at this point we have `self._indexed_same(other)`

        if fill_value is None:
            # since _arith_op may be called in a loop, avoid function call
            #  overhead if possible by doing this check once
            _arith_op = func

        else:

            def _arith_op(left, right):
                # for the mixed_type case where we iterate over columns,
                # _arith_op(left, right) is equivalent to
                # left._binop(right, func, fill_value=fill_value)
                left, right = ops.fill_binop(left, right, fill_value)
                return func(left, right)

        if ops.should_series_dispatch(self, other, func):
            # iterate over columns
            new_data = ops.dispatch_to_series(self, other, _arith_op)
        else:
            with np.errstate(all="ignore"):
                res_values = _arith_op(self.values, other.values)
            new_data = dispatch_fill_zeros(func, self.values, other.values, res_values)

        return new_data
