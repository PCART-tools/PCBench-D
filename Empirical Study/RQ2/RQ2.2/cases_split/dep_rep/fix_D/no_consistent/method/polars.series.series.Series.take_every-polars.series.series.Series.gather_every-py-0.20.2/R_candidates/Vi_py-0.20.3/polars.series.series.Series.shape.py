    @property
    def shape(self) -> tuple[int]:
        """Shape of this Series."""
        return (self._s.len(),)
