    def get_geometry(self):
        """Get the subplot geometry (``n_rows, n_cols, row, col``).

        Unlike SuplorParams, indexes are 0-based.
        """
        rows, cols = self.get_gridspec().get_geometry()
        return rows, cols, self.num1, self.num2
