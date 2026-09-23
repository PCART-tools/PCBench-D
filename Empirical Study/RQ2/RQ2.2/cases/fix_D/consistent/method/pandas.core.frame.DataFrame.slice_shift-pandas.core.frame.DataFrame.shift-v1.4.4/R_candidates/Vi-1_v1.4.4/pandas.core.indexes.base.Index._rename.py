    @final
    def _rename(self: _IndexT, name: Hashable) -> _IndexT:
        """
        fastpath for rename if new name is already validated.
        """
        result = self._view()
        result._name = name
        return result
