    def _reindex_axes(self, axes, level, limit, method, fill_value, copy):
        """ perform the reinxed for all the axes """
        obj = self
        for a in self._AXIS_ORDERS:
            labels = axes[a]
            if labels is None:
                continue

            ax = self._get_axis(a)
            new_index, indexer = ax.reindex(
                labels, level=level, limit=limit, method=method)

            axis = self._get_axis_number(a)
            obj = obj._reindex_with_indexers(
                {axis: [new_index, indexer]}, method=method,
                fill_value=fill_value, limit=limit, copy=copy,
                allow_dups=False)

        return obj
