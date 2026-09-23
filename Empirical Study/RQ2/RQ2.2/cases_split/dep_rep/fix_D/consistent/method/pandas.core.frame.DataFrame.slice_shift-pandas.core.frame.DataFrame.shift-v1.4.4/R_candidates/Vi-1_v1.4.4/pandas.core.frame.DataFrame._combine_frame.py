    def _combine_frame(self, other: DataFrame, func, fill_value=None):
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

        new_data = self._dispatch_frame_op(other, _arith_op)
        return new_data
