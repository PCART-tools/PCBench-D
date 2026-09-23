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

        changed = False
        for lev, lab in zip(self.levels, self.labels):

            uniques = algos.unique(lab)

            # nothing unused
            if len(uniques) == len(lev):
                new_levels.append(lev)
                new_labels.append(lab)
                continue

            changed = True

            # labels get mapped from uniques to 0:len(uniques)
            label_mapping = np.zeros(len(lev))
            label_mapping[uniques] = np.arange(len(uniques))
            lab = label_mapping[lab]

            # new levels are simple
            lev = lev.take(uniques)

            new_levels.append(lev)
            new_labels.append(lab)

        result = self._shallow_copy()

        if changed:
            result._reset_identity()
            result._set_levels(new_levels, validate=False)
            result._set_labels(new_labels, validate=False)

        return result
