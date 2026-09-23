    def add_cell(self, row, col, *args, **kwargs):
        """
        Create a cell and add it to the table.

        Parameters
        ----------
        row : int
            Row index.
        col : int
            Column index.
        *args, **kwargs
            All other parameters are passed on to `Cell`.

        Returns
        -------
        cell : `.CustomCell`
            The created cell.

        """
        xy = (0, 0)
        cell = CustomCell(xy, visible_edges=self.edges, *args, **kwargs)
        self[row, col] = cell
        return cell
