    @_api.deprecated("3.3", alternative="rowspan, colspan")
    def get_rows_columns(self):
        """
        Return the subplot row and column numbers as a tuple
        ``(n_rows, n_cols, row_start, row_stop, col_start, col_stop)``.
        """
        gridspec = self.get_gridspec()
        nrows, ncols = gridspec.get_geometry()
        row_start, col_start = divmod(self.num1, ncols)
        row_stop, col_stop = divmod(self.num2, ncols)
        return nrows, ncols, row_start, row_stop, col_start, col_stop
