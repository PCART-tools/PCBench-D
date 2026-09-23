    def get_geometry(self):
        """
        Return the subplot geometry as tuple ``(n_rows, n_cols, start, stop)``.

        The indices *start* and *stop* define the range of the subplot within
        the `GridSpec`. *stop* is inclusive (i.e. for a single cell
        ``start == stop``).
        """
        rows, cols = self.get_gridspec().get_geometry()
        return rows, cols, self.num1, self.num2
