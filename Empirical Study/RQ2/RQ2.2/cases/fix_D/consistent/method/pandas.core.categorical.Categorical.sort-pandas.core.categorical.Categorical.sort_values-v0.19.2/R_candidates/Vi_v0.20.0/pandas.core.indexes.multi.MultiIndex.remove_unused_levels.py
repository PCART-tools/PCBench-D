    def remove_unused_levels(self):
        """
        create a new MultiIndex from the current that removing
        unused levels, meaning that they are not expressed in the labels

        The resulting MultiIndex will have the same outward
        appearance, meaning the same .values and ordering. It will also
        be .equals() to the original.

        .. versionadded:: 0.20.0

        Returns
        -------
        MultiIndex

        Examples
        --------
        >>> i = pd.MultiIndex.from_product([range(2), list('ab')])
        MultiIndex(levels=[[0, 1], ['a', 'b']],
                   labels=[[0, 0, 1, 1], [0, 1, 0, 1]])


        >>> i[2:]
        MultiIndex(levels=[[0, 1], ['a', 'b']],
                   labels=[[1, 1], [0, 1]])

        The 0 from the first level is not represented
        and can be removed

        >>> i[2:].remove_unused_levels()
        MultiIndex(levels=[[1], ['a', 'b']],
                   labels=[[0, 0], [0, 1]])

        """

        new_levels = []
        new_labels = []

        changed = np.ones(self.nlevels, dtype=bool)
        for i, (lev, lab) in enumerate(zip(self.levels, self.labels)):

            uniques = algos.unique(lab)

            # nothing unused
            if len(uniques) == len(lev):
                new_levels.append(lev)
                new_labels.append(lab)
                changed[i] = False
                continue

            # set difference, then reverse sort
            diff = Index(np.arange(len(lev))).difference(uniques)
            unused = diff.sort_values(ascending=False)

            # new levels are simple
            lev = lev.take(uniques)

            # new labels, we remove the unsued
            # by decrementing the labels for that value
            # prob a better way
            for u in unused:

                lab = np.where(lab > u, lab - 1, lab)

            new_levels.append(lev)
            new_labels.append(lab)

        # nothing changed
        if not changed.any():
            return self

        return MultiIndex(new_levels, new_labels,
                          names=self.names, sortorder=self.sortorder,
                          verify_integrity=False)
