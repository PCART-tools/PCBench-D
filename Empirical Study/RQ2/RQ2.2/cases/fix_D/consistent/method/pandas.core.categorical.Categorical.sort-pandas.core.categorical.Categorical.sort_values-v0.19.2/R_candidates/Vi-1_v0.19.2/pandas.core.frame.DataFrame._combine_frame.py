    def _combine_frame(self, other, func, fill_value=None, level=None):
        this, other = self.align(other, join='outer', level=level, copy=False)
        new_index, new_columns = this.index, this.columns

        def _arith_op(left, right):
            if fill_value is not None:
                left_mask = isnull(left)
                right_mask = isnull(right)
                left = left.copy()
                right = right.copy()

                # one but not both
                mask = left_mask ^ right_mask
                left[left_mask & mask] = fill_value
                right[right_mask & mask] = fill_value

            return func(left, right)

        if this._is_mixed_type or other._is_mixed_type:

            # unique
            if this.columns.is_unique:

                def f(col):
                    r = _arith_op(this[col].values, other[col].values)
                    return self._constructor_sliced(r, index=new_index,
                                                    dtype=r.dtype)

                result = dict([(col, f(col)) for col in this])

            # non-unique
            else:

                def f(i):
                    r = _arith_op(this.iloc[:, i].values,
                                  other.iloc[:, i].values)
                    return self._constructor_sliced(r, index=new_index,
                                                    dtype=r.dtype)

                result = dict([
                    (i, f(i)) for i, col in enumerate(this.columns)
                ])
                result = self._constructor(result, index=new_index, copy=False)
                result.columns = new_columns
                return result

        else:
            result = _arith_op(this.values, other.values)

        return self._constructor(result, index=new_index, columns=new_columns,
                                 copy=False)
