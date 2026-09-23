    def _reindex_axes(self, axes, level, limit, method, fill_value, copy,
                      takeable=False):
        """ perform the reinxed for all the axes """
        obj = self
        for a in self._AXIS_ORDERS:
            labels = axes[a]
            if labels is None:
                continue

            # convert to an index if we are not a multi-selection
            if level is None:
                labels = _ensure_index(labels)

            axis = self._get_axis_number(a)
            ax = self._get_axis(a)
            try:
                new_index, indexer = ax.reindex(
                    labels, level=level, limit=limit, method=method,
                    takeable=takeable)
            except (ValueError):

                # catch trying to reindex a non-monotonic index with a
                # specialized indexer e.g. pad, so fallback to the regular
                # indexer this will show up on reindexing a not-naturally
                # ordering series,
                # e.g.
                # Series(
                #     [1,2,3,4], index=['a','b','c','d']
                # ).reindex(['c','b','g'], method='pad')
                new_index, indexer = ax.reindex(
                    labels, level=level, limit=limit, method=None,
                    takeable=takeable)

            obj = obj._reindex_with_indexers(
                {axis: [new_index, indexer]}, method=method,
                fill_value=fill_value, limit=limit, copy=copy)

        return obj
