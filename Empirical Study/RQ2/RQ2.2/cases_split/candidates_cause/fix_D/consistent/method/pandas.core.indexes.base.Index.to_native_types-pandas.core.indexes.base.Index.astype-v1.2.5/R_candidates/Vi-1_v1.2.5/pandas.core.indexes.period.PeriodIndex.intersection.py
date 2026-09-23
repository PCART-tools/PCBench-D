    def intersection(self, other, sort=False):
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, _ = self._convert_can_do_setop(other)

        if self.equals(other):
            if self.has_duplicates:
                return self.unique()._get_reconciled_name_object(other)
            return self._get_reconciled_name_object(other)

        return self._intersection(other, sort=sort)
