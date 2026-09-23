    @property
    def _header_row_num(self) -> int:
        """Number of rows in header."""
        return self.header_levels if self.fmt.header else 0
