    def _get_gross_column_widths(self) -> Sequence[int]:
        """Get widths of columns containing both headers and actual content."""
        body_column_widths = self._get_body_column_widths()
        return [
            max(*widths)
            for widths in zip(self.header_column_widths, body_column_widths)
        ]
