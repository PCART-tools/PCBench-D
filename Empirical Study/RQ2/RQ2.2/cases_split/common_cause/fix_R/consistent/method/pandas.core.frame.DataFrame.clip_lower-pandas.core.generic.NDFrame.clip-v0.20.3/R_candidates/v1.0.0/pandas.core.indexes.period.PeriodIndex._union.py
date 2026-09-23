    def _union(self, other, sort):
        if not len(other) or self.equals(other) or not len(self):
            return super()._union(other, sort=sort)

        # We are called by `union`, which is responsible for this validation
        assert isinstance(other, type(self))

        if not is_dtype_equal(self.dtype, other.dtype):
            this = self.astype("O")
            other = other.astype("O")
            return this._union(other, sort=sort)

        i8self = Int64Index._simple_new(self.asi8)
        i8other = Int64Index._simple_new(other.asi8)
        i8result = i8self._union(i8other, sort=sort)

        res_name = get_op_result_name(self, other)
        result = self._shallow_copy(np.asarray(i8result, dtype=np.int64), name=res_name)
        return result
