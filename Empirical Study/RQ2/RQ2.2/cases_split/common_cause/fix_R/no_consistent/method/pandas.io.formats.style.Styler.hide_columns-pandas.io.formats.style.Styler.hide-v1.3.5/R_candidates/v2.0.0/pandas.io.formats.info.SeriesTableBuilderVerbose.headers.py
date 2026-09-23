    @property
    def headers(self) -> Sequence[str]:
        """Headers names of the columns in verbose table."""
        if self.with_counts:
            return ["Non-Null Count", "Dtype"]
        return ["Dtype"]
