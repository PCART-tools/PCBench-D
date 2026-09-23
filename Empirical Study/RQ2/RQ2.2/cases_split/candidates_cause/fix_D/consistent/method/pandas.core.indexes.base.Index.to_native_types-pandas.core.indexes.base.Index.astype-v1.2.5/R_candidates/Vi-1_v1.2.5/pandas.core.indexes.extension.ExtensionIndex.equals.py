    @doc(Index.equals)
    def equals(self, other) -> bool:
        # Dispatch to the ExtensionArray's .equals method.
        if self.is_(other):
            return True

        if not isinstance(other, type(self)):
            return False

        return self._data.equals(other._data)
