    def __getitem__(self, position):
        """
        Retrieve a custom cell from a given position.
        """
        try:
            row, col = position[0], position[1]
        except Exception:
            raise KeyError('Only tuples length 2 are accepted as coordinates')
        return self._cells[row, col]
