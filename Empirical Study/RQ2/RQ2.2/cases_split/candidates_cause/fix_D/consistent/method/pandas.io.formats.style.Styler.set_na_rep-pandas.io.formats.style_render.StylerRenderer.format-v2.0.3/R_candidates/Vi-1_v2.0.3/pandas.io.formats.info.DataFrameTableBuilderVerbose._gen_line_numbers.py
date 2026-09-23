    def _gen_line_numbers(self) -> Iterator[str]:
        """Iterator with string representation of column numbers."""
        for i, _ in enumerate(self.ids):
            yield f" {i}"
