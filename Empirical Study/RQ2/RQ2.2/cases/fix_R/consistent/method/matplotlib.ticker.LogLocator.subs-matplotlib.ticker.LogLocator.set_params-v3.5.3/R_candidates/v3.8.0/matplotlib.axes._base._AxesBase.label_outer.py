    def label_outer(self, remove_inner_ticks=False):
        """
        Only show "outer" labels and tick labels.

        x-labels are only kept for subplots on the last row (or first row, if
        labels are on the top side); y-labels only for subplots on the first
        column (or last column, if labels are on the right side).

        Parameters
        ----------
        remove_inner_ticks : bool, default: False
            If True, remove the inner ticks as well (not only tick labels).

            .. versionadded:: 3.8
        """
        self._label_outer_xaxis(skip_non_rectangular_axes=False,
                                remove_inner_ticks=remove_inner_ticks)
        self._label_outer_yaxis(skip_non_rectangular_axes=False,
                                remove_inner_ticks=remove_inner_ticks)
