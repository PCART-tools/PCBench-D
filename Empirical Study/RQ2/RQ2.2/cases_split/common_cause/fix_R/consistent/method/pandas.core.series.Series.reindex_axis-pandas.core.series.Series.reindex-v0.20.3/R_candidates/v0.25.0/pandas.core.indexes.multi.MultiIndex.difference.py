    def difference(self, other, sort=None):
        """
        Compute set difference of two MultiIndex objects

        Parameters
        ----------
        other : MultiIndex
        sort : False or None, default None
            Sort the resulting MultiIndex if possible

            .. versionadded:: 0.24.0

            .. versionchanged:: 0.24.1

               Changed the default value from ``True`` to ``None``
               (without change in behaviour).

        Returns
        -------
        diff : MultiIndex
        """
        self._validate_sort_keyword(sort)
        self._assert_can_do_setop(other)
        other, result_names = self._convert_can_do_setop(other)

        if len(other) == 0:
            return self

        if self.equals(other):
            return MultiIndex(
                levels=self.levels,
                codes=[[]] * self.nlevels,
                names=result_names,
                verify_integrity=False,
            )

        this = self._get_unique_index()

        indexer = this.get_indexer(other)
        indexer = indexer.take((indexer != -1).nonzero()[0])

        label_diff = np.setdiff1d(np.arange(this.size), indexer, assume_unique=True)
        difference = this.values.take(label_diff)
        if sort is None:
            difference = sorted(difference)

        if len(difference) == 0:
            return MultiIndex(
                levels=[[]] * self.nlevels,
                codes=[[]] * self.nlevels,
                names=result_names,
                verify_integrity=False,
            )
        else:
            return MultiIndex.from_tuples(difference, sortorder=0, names=result_names)
