    def intersection(self, other):
        """
        Form the intersection of two MultiIndex objects, sorting if possible

        Parameters
        ----------
        other : MultiIndex or array / Index of tuples

        Returns
        -------
        Index
        """
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if self.equals(other):
            return self

        self_tuples = self._values
        other_tuples = other._values
        uniq_tuples = sorted(set(self_tuples) & set(other_tuples))
        if len(uniq_tuples) == 0:
            return MultiIndex(levels=[[]] * self.nlevels,
                              labels=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)
        else:
            return MultiIndex.from_arrays(lzip(*uniq_tuples), sortorder=0,
                                          names=result_names)
