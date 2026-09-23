    def get_grid_positions(self, fig):
        """
        return lists of bottom and top position of rows, left and
        right positions of columns.
        """
        nrows, ncols = self.get_geometry()

        subplot_params = self.get_subplot_params(fig)
        left = subplot_params.left
        right = subplot_params.right
        bottom = subplot_params.bottom
        top = subplot_params.top
        wspace = subplot_params.wspace
        hspace = subplot_params.hspace
        totWidth = right - left
        totHeight = top - bottom

        # calculate accumulated heights of columns
        cellH = totHeight / (nrows + hspace*(nrows-1))
        sepH = hspace * cellH
        if self._row_height_ratios is not None:
            netHeight = cellH * nrows
            tr = float(sum(self._row_height_ratios))
            cellHeights = [netHeight * r / tr for r in self._row_height_ratios]
        else:
            cellHeights = [cellH] * nrows
        sepHeights = [0] + ([sepH] * (nrows-1))
        cellHs = np.cumsum(np.column_stack([sepHeights, cellHeights]).flat)

        # calculate accumulated widths of rows
        cellW = totWidth/(ncols + wspace*(ncols-1))
        sepW = wspace*cellW
        if self._col_width_ratios is not None:
            netWidth = cellW * ncols
            tr = float(sum(self._col_width_ratios))
            cellWidths = [netWidth*r/tr for r in self._col_width_ratios]
        else:
            cellWidths = [cellW] * ncols
        sepWidths = [0] + ([sepW] * (ncols-1))
        cellWs = np.cumsum(np.column_stack([sepWidths, cellWidths]).flat)

        figTops = [top - cellHs[2*rowNum] for rowNum in range(nrows)]
        figBottoms = [top - cellHs[2*rowNum+1] for rowNum in range(nrows)]
        figLefts = [left + cellWs[2*colNum] for colNum in range(ncols)]
        figRights = [left + cellWs[2*colNum+1] for colNum in range(ncols)]

        return figBottoms, figTops, figLefts, figRights
