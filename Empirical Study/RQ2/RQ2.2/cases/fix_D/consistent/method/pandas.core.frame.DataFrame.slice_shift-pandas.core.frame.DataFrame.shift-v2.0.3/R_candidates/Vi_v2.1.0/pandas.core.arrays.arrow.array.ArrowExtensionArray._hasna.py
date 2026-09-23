    @property
    def _hasna(self) -> bool:
        return self._pa_array.null_count > 0
