    def add_cell(self, row, col, *args, **kwargs):
        """ Add a cell to the table. """
        xy = (0, 0)

        cell = CustomCell(xy, visible_edges=self.edges, *args, **kwargs)
        cell.set_figure(self.figure)
        cell.set_transform(self.get_transform())

        cell.set_clip_on(False)
        self._cells[row, col] = cell
        self.stale = True
