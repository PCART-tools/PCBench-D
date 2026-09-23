    def sortlevel(self, level=0, ascending=True, sort_remaining=True):
        """
        Sort MultiIndex at the requested level. The result will respect the
        original ordering of the associated factor at that level.

        Parameters
        ----------
        level : list-like, int or str, default 0
            If a string is given, must be a name of the level
            If list-like must be names or ints of levels.
        ascending : boolean, default True
            False to sort in descending order
        sort_remaining : sort by the remaining levels after level.

        Returns
        -------
        sorted_index : MultiIndex
        """
        from pandas.core.groupby import _indexer_from_factorized

        labels = list(self.labels)
        shape = list(self.levshape)

        if isinstance(level, (str, int)):
            level = [level]
        level = [self._get_level_number(lev) for lev in level]

        # partition labels and shape
        primary = tuple(labels.pop(lev - i) for i, lev in enumerate(level))
        primshp = tuple(shape.pop(lev - i) for i, lev in enumerate(level))

        if sort_remaining:
            primary += primary + tuple(labels)
            primshp += primshp + tuple(shape)
            sortorder = None
        else:
            sortorder = level[0]

        indexer = _indexer_from_factorized(primary,
                                           primshp,
                                           compress=False)

        if not ascending:
            indexer = indexer[::-1]

        indexer = com._ensure_platform_int(indexer)
        new_labels = [lab.take(indexer) for lab in self.labels]

        new_index = MultiIndex(labels=new_labels, levels=self.levels,
                               names=self.names, sortorder=sortorder,
                               verify_integrity=False)

        return new_index, indexer
