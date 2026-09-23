    def difference(self, other):
        """
        Compute sorted set difference of two MultiIndex objects

        Returns
        -------
        diff : MultiIndex
        """
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if len(other) == 0:
            return self

        if self.equals(other):
            return MultiIndex(levels=[[]] * self.nlevels,
                              labels=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)

        difference = sorted(set(self._values) - set(other._values))

        if len(difference) == 0:
            return MultiIndex(levels=[[]] * self.nlevels,
                              labels=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)
        else:
            return MultiIndex.from_tuples(difference, sortorder=0,
                                          names=result_names)
