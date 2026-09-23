    def _reindex_axes(
        self: NDFrameT, axes, level, limit, tolerance, method, fill_value, copy
    ) -> NDFrameT:
        """Perform the reindex for all the axes."""
        obj = self
        for a in self._AXIS_ORDERS:
            labels = axes[a]
            if labels is None:
                continue

            ax = self._get_axis(a)
            new_index, indexer = ax.reindex(
                labels, level=level, limit=limit, tolerance=tolerance, method=method
            )

            axis = self._get_axis_number(a)
            obj = obj._reindex_with_indexers(
                {axis: [new_index, indexer]},
                fill_value=fill_value,
                copy=copy,
                allow_dups=False,
            )
            # If we've made a copy once, no need to make another one
            copy = False

        return obj
