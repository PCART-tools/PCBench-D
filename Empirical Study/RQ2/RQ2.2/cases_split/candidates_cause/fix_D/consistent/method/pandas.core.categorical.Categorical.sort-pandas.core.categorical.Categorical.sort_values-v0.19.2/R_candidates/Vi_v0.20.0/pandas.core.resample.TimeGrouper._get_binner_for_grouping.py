    def _get_binner_for_grouping(self, obj):
        # return an ordering of the transformed group labels,
        # suitable for multi-grouping, e.g the labels for
        # the resampled intervals
        binner, grouper, obj = self._get_grouper(obj)

        l = []
        for key, group in grouper.get_iterator(self.ax):
            l.extend([key] * len(group))

        if isinstance(self.ax, PeriodIndex):
            grouper = binner.__class__(l, freq=binner.freq, name=binner.name)
        else:
            # resampling causes duplicated values, specifying freq is invalid
            grouper = binner.__class__(l, name=binner.name)

        # since we may have had to sort
        # may need to reorder groups here
        if self.indexer is not None:
            indexer = self.indexer.argsort(kind='quicksort')
            grouper = grouper.take(indexer)
        return grouper
