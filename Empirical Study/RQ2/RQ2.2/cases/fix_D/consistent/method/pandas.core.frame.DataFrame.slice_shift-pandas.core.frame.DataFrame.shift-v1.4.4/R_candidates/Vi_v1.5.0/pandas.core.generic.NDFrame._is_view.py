    @final
    @property
    def _is_view(self) -> bool_t:
        """Return boolean indicating if self is view of another array"""
        return self._mgr.is_view
