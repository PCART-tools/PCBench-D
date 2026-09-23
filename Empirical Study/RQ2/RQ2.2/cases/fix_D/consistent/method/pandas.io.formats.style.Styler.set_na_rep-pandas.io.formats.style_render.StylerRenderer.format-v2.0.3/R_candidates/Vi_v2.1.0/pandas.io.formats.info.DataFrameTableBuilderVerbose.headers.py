    @property
    def headers(self) -> Sequence[str]:
        """Headers names of the columns in verbose table."""
        if self.with_counts:
            return [" # ", "Column", "Non-Null Count", "Dtype"]
        return [" # ", "Column", "Dtype"]
