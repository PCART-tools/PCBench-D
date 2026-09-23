    def __setitem__(self, position, cell):
        """
        Set a custom cell in a given position.
        """
        cbook._check_isinstance(CustomCell, cell=cell)
        try:
            row, col = position[0], position[1]
        except Exception:
            raise KeyError('Only tuples length 2 are accepted as coordinates')
        cell.set_figure(self.figure)
        cell.set_transform(self.get_transform())
        cell.set_clip_on(False)
        self._cells[row, col] = cell
        self.stale = True
