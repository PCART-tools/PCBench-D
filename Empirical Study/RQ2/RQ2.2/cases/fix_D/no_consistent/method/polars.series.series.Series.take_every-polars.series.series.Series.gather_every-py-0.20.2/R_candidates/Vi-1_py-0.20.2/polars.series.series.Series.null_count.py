    def null_count(self) -> int:
        """Count the null values in this Series."""
        return self._s.null_count()
