    def _union(self, other, sort):
        if not len(other) or self.equals(other) or not len(self):
            return super()._union(other, sort=sort)

        # We are called by `union`, which is responsible for this validation
        assert isinstance(other, type(self))

        if not is_dtype_equal(self.dtype, other.dtype):
            this = self.astype("O")
            other = other.astype("O")
            return this._union(other, sort=sort)

        return self._setop(other, sort, opname="_union")
