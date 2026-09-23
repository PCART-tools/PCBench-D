    def add_cell(self, row, col, *args, **kwargs):
        """
        Add a cell to the table.

        Parameters
        ----------
        row : int
            Row index.
        col : int
            Column index.

        Returns
        -------
        `CustomCell`: Automatically created cell

        """
        xy = (0, 0)
        cell = CustomCell(xy, visible_edges=self.edges, *args, **kwargs)
        self[row, col] = cell
        return cell
