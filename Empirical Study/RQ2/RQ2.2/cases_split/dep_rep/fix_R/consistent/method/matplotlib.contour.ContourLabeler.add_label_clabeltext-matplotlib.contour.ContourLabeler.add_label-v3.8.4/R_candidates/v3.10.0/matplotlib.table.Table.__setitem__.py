    def __setitem__(self, position, cell):
        """
        Set a custom cell in a given position.
        """
        _api.check_isinstance(Cell, cell=cell)
        try:
            row, col = position[0], position[1]
        except Exception as err:
            raise KeyError('Only tuples length 2 are accepted as '
                           'coordinates') from err
        cell.set_figure(self.get_figure(root=False))
        cell.set_transform(self.get_transform())
        cell.set_clip_on(False)
        self._cells[row, col] = cell
        self.stale = True
