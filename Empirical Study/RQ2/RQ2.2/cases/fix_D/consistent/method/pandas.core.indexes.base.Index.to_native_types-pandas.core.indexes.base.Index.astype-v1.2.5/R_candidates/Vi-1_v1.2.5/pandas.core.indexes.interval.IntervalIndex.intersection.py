    @Appender(Index.intersection.__doc__)
    def intersection(self, other, sort=False) -> Index:
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, _ = self._convert_can_do_setop(other)

        if self.equals(other):
            if self.has_duplicates:
                return self.unique()._get_reconciled_name_object(other)
            return self._get_reconciled_name_object(other)

        if not isinstance(other, IntervalIndex):
            return self.astype(object).intersection(other)

        result = self._intersection(other, sort=sort)
        return self._wrap_setop_result(other, result)
