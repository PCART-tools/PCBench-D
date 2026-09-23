    def _get_index_format(self) -> str:
        """Get index column format."""
        return "l" * self.frame.index.nlevels if self.fmt.index else ""
