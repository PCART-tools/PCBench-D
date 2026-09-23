    def diff(self, other):
        """
        Compute sorted set difference of two MultiIndex objects

        Returns
        -------
        diff : MultiIndex
        """
        self._assert_can_do_setop(other)

        if not isinstance(other, MultiIndex):
            if len(other) == 0:
                return self
            try:
                other = MultiIndex.from_tuples(other)
            except:
                raise TypeError('other must be a MultiIndex or a list of'
                                ' tuples')
            result_names = self.names
        else:
            result_names = self.names if self.names == other.names else None

        if self.equals(other):
            return MultiIndex(levels=[[]] * self.nlevels,
                              labels=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)

        difference = sorted(set(self.values) - set(other.values))

        if len(difference) == 0:
            return MultiIndex(levels=[[]] * self.nlevels,
                              labels=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)
        else:
            return MultiIndex.from_tuples(difference, sortorder=0,
                                          names=result_names)
