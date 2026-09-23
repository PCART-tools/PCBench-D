    def add_index_range_line(self) -> None:
        """Add line with range of indices to the table."""
        self._lines.append(self.data.index._summary())
