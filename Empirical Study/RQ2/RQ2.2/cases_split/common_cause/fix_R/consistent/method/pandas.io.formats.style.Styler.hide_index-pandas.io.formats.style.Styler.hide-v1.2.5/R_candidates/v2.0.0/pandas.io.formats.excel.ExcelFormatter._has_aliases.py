    @property
    def _has_aliases(self) -> bool:
        """Whether the aliases for column names are present."""
        return is_list_like(self.header)
