    def difference(self, other, sort=True):
        """
        Compute set difference of two MultiIndex objects

        Parameters
        ----------
        other : MultiIndex
        sort : bool, default True
            Sort the resulting MultiIndex if possible

            .. versionadded:: 0.24.0

        Returns
        -------
        diff : MultiIndex
        """
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if len(other) == 0:
            return self

        if self.equals(other):
            return MultiIndex(levels=self.levels,
                              codes=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)

        this = self._get_unique_index()

        indexer = this.get_indexer(other)
        indexer = indexer.take((indexer != -1).nonzero()[0])

        label_diff = np.setdiff1d(np.arange(this.size), indexer,
                                  assume_unique=True)
        difference = this.values.take(label_diff)
        if sort:
            difference = sorted(difference)

        if len(difference) == 0:
            return MultiIndex(levels=[[]] * self.nlevels,
                              codes=[[]] * self.nlevels,
                              names=result_names, verify_integrity=False)
        else:
            return MultiIndex.from_tuples(difference, sortorder=0,
                                          names=result_names)
