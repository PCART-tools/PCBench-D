    def get_grid_positions(self, fig, raw=False):
        """
        return lists of bottom and top position of rows, left and
        right positions of columns.

        If raw=True, then these are all in units relative to the container
        with no margins.  (used for constrained_layout).
        """
        nrows, ncols = self.get_geometry()

        if raw:
            left = 0.
            right = 1.
            bottom = 0.
            top = 1.
            wspace = 0.
            hspace = 0.
        else:
            subplot_params = self.get_subplot_params(fig)
            left = subplot_params.left
            right = subplot_params.right
            bottom = subplot_params.bottom
            top = subplot_params.top
            wspace = subplot_params.wspace
            hspace = subplot_params.hspace
        tot_width = right - left
        tot_height = top - bottom

        # calculate accumulated heights of columns
        cell_h = tot_height / (nrows + hspace*(nrows-1))
        sep_h = hspace * cell_h
        if self._row_height_ratios is not None:
            norm = cell_h * nrows / sum(self._row_height_ratios)
            cell_heights = [r * norm for r in self._row_height_ratios]
        else:
            cell_heights = [cell_h] * nrows
        sep_heights = [0] + ([sep_h] * (nrows-1))
        cell_hs = np.cumsum(np.column_stack([sep_heights, cell_heights]).flat)

        # calculate accumulated widths of rows
        cell_w = tot_width / (ncols + wspace*(ncols-1))
        sep_w = wspace * cell_w
        if self._col_width_ratios is not None:
            norm = cell_w * ncols / sum(self._col_width_ratios)
            cell_widths = [r * norm for r in self._col_width_ratios]
        else:
            cell_widths = [cell_w] * ncols
        sep_widths = [0] + ([sep_w] * (ncols-1))
        cell_ws = np.cumsum(np.column_stack([sep_widths, cell_widths]).flat)

        fig_tops, fig_bottoms = (top - cell_hs).reshape((-1, 2)).T
        fig_lefts, fig_rights = (left + cell_ws).reshape((-1, 2)).T
        return fig_bottoms, fig_tops, fig_lefts, fig_rights
