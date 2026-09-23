    def _setop(self, other, sort, opname: str):
        """
        Perform a set operation by dispatching to the Int64Index implementation.
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        res_name = get_op_result_name(self, other)
        other = ensure_index(other)

        i8self = Int64Index._simple_new(self.asi8)
        i8other = Int64Index._simple_new(other.asi8)
        i8result = getattr(i8self, opname)(i8other, sort=sort)

        parr = type(self._data)(np.asarray(i8result, dtype=np.int64), dtype=self.dtype)
        result = type(self)._simple_new(parr, name=res_name)
        return result
