    def get_position(self, figure, return_all=False):
        """
        Update the subplot position from ``figure.subplotpars``.
        """
        gridspec = self.get_gridspec()
        nrows, ncols = gridspec.get_geometry()
        rows, cols = np.unravel_index([self.num1, self.num2], (nrows, ncols))
        fig_bottoms, fig_tops, fig_lefts, fig_rights = \
            gridspec.get_grid_positions(figure)

        fig_bottom = fig_bottoms[rows].min()
        fig_top = fig_tops[rows].max()
        fig_left = fig_lefts[cols].min()
        fig_right = fig_rights[cols].max()
        figbox = Bbox.from_extents(fig_left, fig_bottom, fig_right, fig_top)

        if return_all:
            return figbox, rows[0], cols[0], nrows, ncols
        else:
            return figbox
