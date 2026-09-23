    @property
    def is_view(self):
        """Extension arrays are never treated as views."""
        return False
