    @property
    def fields(self) -> list[str]:
        """Get the names of the fields."""
        if getattr(self, "_s", None) is None:
            return []
        return self._s.struct_fields()
