    def _combine_frame(self, other, func, fill_value=None, level=None):
        this, other = self.align(other, join='outer', level=level, copy=False)
        new_index, new_columns = this.index, this.columns

        def _arith_op(left, right):
            # for the mixed_type case where we iterate over columns,
            # _arith_op(left, right) is equivalent to
            # left._binop(right, func, fill_value=fill_value)
            left, right = ops.fill_binop(left, right, fill_value)
            return func(left, right)

        if this._is_mixed_type or other._is_mixed_type:
            # iterate over columns
            if this.columns.is_unique:
                # unique columns
                result = {col: _arith_op(this[col], other[col])
                          for col in this}
                result = self._constructor(result, index=new_index,
                                           columns=new_columns, copy=False)
            else:
                # non-unique columns
                result = {i: _arith_op(this.iloc[:, i], other.iloc[:, i])
                          for i, col in enumerate(this.columns)}
                result = self._constructor(result, index=new_index, copy=False)
                result.columns = new_columns
            return result

        else:
            result = _arith_op(this.values, other.values)

        return self._constructor(result, index=new_index, columns=new_columns,
                                 copy=False)
