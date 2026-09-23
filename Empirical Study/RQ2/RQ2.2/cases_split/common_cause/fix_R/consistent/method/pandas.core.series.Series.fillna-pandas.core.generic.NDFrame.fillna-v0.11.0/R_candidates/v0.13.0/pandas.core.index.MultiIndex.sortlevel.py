    def sortlevel(self, level=0, ascending=True):
        """
        Sort MultiIndex at the requested level. The result will respect the
        original ordering of the associated factor at that level.

        Parameters
        ----------
        level : int or str, default 0
            If a string is given, must be a name of the level
        ascending : boolean, default True
            False to sort in descending order

        Returns
        -------
        sorted_index : MultiIndex
        """
        from pandas.core.groupby import _indexer_from_factorized

        labels = list(self.labels)

        level = self._get_level_number(level)
        primary = labels.pop(level)

        shape = list(self.levshape)
        primshp = shape.pop(level)

        indexer = _indexer_from_factorized((primary,) + tuple(labels),
                                           (primshp,) + tuple(shape),
                                           compress=False)
        if not ascending:
            indexer = indexer[::-1]

        indexer = com._ensure_platform_int(indexer)
        new_labels = [lab.take(indexer) for lab in self.labels]

        new_index = MultiIndex(labels=new_labels, levels=self.levels,
                               names=self.names, sortorder=level,
                               verify_integrity=False)

        return new_index, indexer
