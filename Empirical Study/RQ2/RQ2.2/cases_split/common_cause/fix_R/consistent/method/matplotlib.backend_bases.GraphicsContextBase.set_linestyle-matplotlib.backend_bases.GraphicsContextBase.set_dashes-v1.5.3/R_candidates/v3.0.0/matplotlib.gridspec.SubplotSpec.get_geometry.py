    def get_geometry(self):
        """
        Get the subplot geometry (``n_rows, n_cols, start, stop``).

        start and stop are the index of the start and stop of the
        subplot.
        """
        rows, cols = self.get_gridspec().get_geometry()
        return rows, cols, self.num1, self.num2
