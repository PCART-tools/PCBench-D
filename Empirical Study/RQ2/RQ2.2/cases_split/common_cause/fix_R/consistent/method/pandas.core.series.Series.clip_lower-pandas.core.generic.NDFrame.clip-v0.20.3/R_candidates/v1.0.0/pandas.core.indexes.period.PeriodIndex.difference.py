    def difference(self, other, sort=None):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        res_name = get_op_result_name(self, other)
        other = ensure_index(other)

        if self.equals(other):
            # pass an empty PeriodArray with the appropriate dtype
            return self._shallow_copy(self._data[:0])

        if is_object_dtype(other):
            return self.astype(object).difference(other).astype(self.dtype)

        elif not is_dtype_equal(self.dtype, other.dtype):
            return self

        i8self = Int64Index._simple_new(self.asi8)
        i8other = Int64Index._simple_new(other.asi8)
        i8result = i8self.difference(i8other, sort=sort)

        result = self._shallow_copy(np.asarray(i8result, dtype=np.int64), name=res_name)
        return result
