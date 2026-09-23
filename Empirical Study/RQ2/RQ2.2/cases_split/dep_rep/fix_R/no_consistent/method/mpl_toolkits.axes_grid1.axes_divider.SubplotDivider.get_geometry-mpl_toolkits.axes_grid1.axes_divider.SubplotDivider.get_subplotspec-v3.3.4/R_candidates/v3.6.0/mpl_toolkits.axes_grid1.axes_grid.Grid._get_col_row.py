    def _get_col_row(self, n):
        if self._direction == "column":
            col, row = divmod(n, self._nrows)
        else:
            row, col = divmod(n, self._ncols)

        return col, row
