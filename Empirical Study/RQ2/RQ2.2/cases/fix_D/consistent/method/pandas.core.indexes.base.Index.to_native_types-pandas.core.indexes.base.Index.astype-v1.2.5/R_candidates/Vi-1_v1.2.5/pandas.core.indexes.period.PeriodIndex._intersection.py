    def _intersection(self, other, sort=False):

        if is_object_dtype(other.dtype):
            return self.astype("O").intersection(other, sort=sort)

        elif not self._is_comparable_dtype(other.dtype):
            # We can infer that the intersection is empty.
            # assert_can_do_setop ensures that this is not just a mismatched freq
            this = self[:0].astype("O")
            other = other[:0].astype("O")
            return this.intersection(other, sort=sort)

        return self._setop(other, sort, opname="intersection")
