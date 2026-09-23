    def layout_from_subplotspec(self, subspec,
                                name='', artist=None, pos=False):
        """
        Make a layout box from a subplotspec. The layout box is
        constrained to be a fraction of the width/height of the parent,
        and be a fraction of the parent width/height from the left/bottom
        of the parent.  Therefore the parent can move around and the
        layout for the subplot spec should move with it.

        The parent is *usually* the gridspec that made the subplotspec.??
        """
        lb = LayoutBox(parent=self, name=name, artist=artist, pos=pos)
        gs = subspec.get_gridspec()
        nrows, ncols = gs.get_geometry()
        parent = self.parent

        # OK, now, we want to set the position of this subplotspec
        # based on its subplotspec parameters.  The new gridspec will inherit
        # from gridspec.  prob should be new method in gridspec
        left = 0.0
        right = 1.0
        bottom = 0.0
        top = 1.0
        totWidth = right-left
        totHeight = top-bottom
        hspace = 0.
        wspace = 0.

        # calculate accumulated heights of columns
        cellH = totHeight / (nrows + hspace * (nrows - 1))
        sepH = hspace * cellH

        if gs._row_height_ratios is not None:
            netHeight = cellH * nrows
            tr = sum(gs._row_height_ratios)
            cellHeights = [netHeight * r / tr for r in gs._row_height_ratios]
        else:
            cellHeights = [cellH] * nrows

        sepHeights = [0] + ([sepH] * (nrows - 1))
        cellHs = np.cumsum(np.column_stack([sepHeights, cellHeights]).flat)

        # calculate accumulated widths of rows
        cellW = totWidth / (ncols + wspace * (ncols - 1))
        sepW = wspace * cellW

        if gs._col_width_ratios is not None:
            netWidth = cellW * ncols
            tr = sum(gs._col_width_ratios)
            cellWidths = [netWidth * r / tr for r in gs._col_width_ratios]
        else:
            cellWidths = [cellW] * ncols

        sepWidths = [0] + ([sepW] * (ncols - 1))
        cellWs = np.cumsum(np.column_stack([sepWidths, cellWidths]).flat)

        figTops = [top - cellHs[2 * rowNum] for rowNum in range(nrows)]
        figBottoms = [top - cellHs[2 * rowNum + 1] for rowNum in range(nrows)]
        figLefts = [left + cellWs[2 * colNum] for colNum in range(ncols)]
        figRights = [left + cellWs[2 * colNum + 1] for colNum in range(ncols)]

        rowNum1, colNum1 = divmod(subspec.num1, ncols)
        rowNum2, colNum2 = divmod(subspec.num2, ncols)
        figBottom = min(figBottoms[rowNum1], figBottoms[rowNum2])
        figTop = max(figTops[rowNum1], figTops[rowNum2])
        figLeft = min(figLefts[colNum1], figLefts[colNum2])
        figRight = max(figRights[colNum1], figRights[colNum2])

        # These are numbers relative to (0, 0, 1, 1).  Need to constrain
        # relative to parent.

        width = figRight - figLeft
        height = figTop - figBottom
        parent = self.parent
        cs = [self.left == parent.left + parent.width * figLeft,
              self.bottom == parent.bottom + parent.height * figBottom,
              self.width == parent.width * width,
              self.height == parent.height * height]
        for c in cs:
            self.solver.addConstraint(c | 'required')

        return lb
