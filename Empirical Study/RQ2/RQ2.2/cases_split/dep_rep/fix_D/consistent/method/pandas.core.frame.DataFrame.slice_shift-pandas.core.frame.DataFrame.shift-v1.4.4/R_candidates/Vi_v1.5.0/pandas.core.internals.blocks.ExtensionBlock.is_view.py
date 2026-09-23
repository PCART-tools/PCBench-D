    @property
    def is_view(self) -> bool:
        """Extension arrays are never treated as views."""
        return False
