    @final
    def _rename(self, name: Hashable) -> Self:
        """
        fastpath for rename if new name is already validated.
        """
        result = self._view()
        result._name = name
        return result
