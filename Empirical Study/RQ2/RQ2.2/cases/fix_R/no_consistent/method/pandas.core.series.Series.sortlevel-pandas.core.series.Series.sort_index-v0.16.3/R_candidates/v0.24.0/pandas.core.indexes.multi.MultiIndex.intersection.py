    def intersection(self, other, sort=True):
        """
        Form the intersection of two MultiIndex objects.

        Parameters
        ----------
        other : MultiIndex or array / Index of tuples
        sort : bool, default True
            Sort the resulting MultiIndex if possible

            .. versionadded:: 0.24.0

        Returns
        -------
        Index
        """
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if self.equals(other):
            return self

        self_tuples = self._ndarray_values
        other_tuples = other._ndarray_values
        uniq_tuples = set(self_tuples) & set(other_tuples)

        if sort:
            uniq_tuples = sorted(uniq_tuples)

        if len(uniq_tuples) == 0:
            return MultiIndex(levels=self.levels,
                              codes=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)
        else:
            return MultiIndex.from_arrays(lzip(*uniq_tuples), sortorder=0,
                                          names=result_names)
