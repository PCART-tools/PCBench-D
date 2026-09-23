    @property
    def _axes_are_unique(self) -> bool:
        # Only relevant for self.ndim == 2
        assert self.ndim == 2
        return self.obj.index.is_unique and self.obj.columns.is_unique
