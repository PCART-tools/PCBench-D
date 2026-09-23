    def intersection(self, other, sort=False):
        """
        Form the intersection of two MultiIndex objects.

        Parameters
        ----------
        other : MultiIndex or array / Index of tuples
        sort : False or None, default False
            Sort the resulting MultiIndex if possible

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default from ``True`` to ``False``, to match
               behaviour from before 0.24.0

        Returns
        -------
        Index
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if self.equals(other):
            if self.has_duplicates:
                return self.unique().rename(result_names)
            return self.rename(result_names)

        return self._intersection(other, sort=sort)
