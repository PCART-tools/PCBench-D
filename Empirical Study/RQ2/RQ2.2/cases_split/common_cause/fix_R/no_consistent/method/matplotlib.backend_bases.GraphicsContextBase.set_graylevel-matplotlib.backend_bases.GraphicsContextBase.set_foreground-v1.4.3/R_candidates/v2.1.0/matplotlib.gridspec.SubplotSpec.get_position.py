    def get_position(self, fig, return_all=False):
        """Update the subplot position from ``fig.subplotpars``.
        """

        gridspec = self.get_gridspec()
        nrows, ncols = gridspec.get_geometry()

        figBottoms, figTops, figLefts, figRights = \
            gridspec.get_grid_positions(fig)

        rowNum, colNum =  divmod(self.num1, ncols)
        figBottom = figBottoms[rowNum]
        figTop = figTops[rowNum]
        figLeft = figLefts[colNum]
        figRight = figRights[colNum]

        if self.num2 is not None:

            rowNum2, colNum2 =  divmod(self.num2, ncols)
            figBottom2 = figBottoms[rowNum2]
            figTop2 = figTops[rowNum2]
            figLeft2 = figLefts[colNum2]
            figRight2 = figRights[colNum2]

            figBottom = min(figBottom, figBottom2)
            figLeft = min(figLeft, figLeft2)
            figTop = max(figTop, figTop2)
            figRight = max(figRight, figRight2)

        figbox = mtransforms.Bbox.from_extents(figLeft, figBottom,
                                               figRight, figTop)

        if return_all:
            return figbox, rowNum, colNum, nrows, ncols
        else:
            return figbox
