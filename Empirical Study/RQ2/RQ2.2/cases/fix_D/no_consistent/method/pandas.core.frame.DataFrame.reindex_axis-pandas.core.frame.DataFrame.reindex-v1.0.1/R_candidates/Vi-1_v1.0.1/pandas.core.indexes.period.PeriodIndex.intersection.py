    def intersection(self, other, sort=False):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        res_name = get_op_result_name(self, other)
        other = ensure_index(other)

        if self.equals(other):
            return self._get_reconciled_name_object(other)

        if not is_dtype_equal(self.dtype, other.dtype):
            # TODO: fastpath for if we have a different PeriodDtype
            this = self.astype("O")
            other = other.astype("O")
            return this.intersection(other, sort=sort)

        i8self = Int64Index._simple_new(self.asi8)
        i8other = Int64Index._simple_new(other.asi8)
        i8result = i8self.intersection(i8other, sort=sort)

        result = self._shallow_copy(np.asarray(i8result, dtype=np.int64), name=res_name)
        return result
