    def difference(self, other, sort=None):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_name = self._convert_can_do_setop(other)

        if self.equals(other):
            return self[:0].rename(result_name)

        return self._difference(other, sort=sort)
