    def intersection(self, other, sort=False):
        """
        Specialized intersection for DatetimeIndex/TimedeltaIndex.

        May be much faster than Index.intersection

        Parameters
        ----------
        other : Same type as self or array-like
        sort : False or None, default False
            Sort the resulting index if possible.

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default to ``False`` to match the behaviour
               from before 0.24.0.

            .. versionchanged:: 0.25.0

               The `sort` keyword is added

        Returns
        -------
        y : Index or same type as self
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, _ = self._convert_can_do_setop(other)

        if self.equals(other):
            if self.has_duplicates:
                return self.unique()._get_reconciled_name_object(other)
            return self._get_reconciled_name_object(other)

        return self._intersection(other, sort=sort)
