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
            return self

        self_tuples = self._ndarray_values
        other_tuples = other._ndarray_values
        uniq_tuples = set(self_tuples) & set(other_tuples)

        if sort is None:
            uniq_tuples = sorted(uniq_tuples)

        if len(uniq_tuples) == 0:
            return MultiIndex(
                levels=self.levels,
                codes=[[]] * self.nlevels,
                names=result_names,
                verify_integrity=False,
            )
        else:
            return MultiIndex.from_arrays(
                zip(*uniq_tuples), sortorder=0, names=result_names
            )
