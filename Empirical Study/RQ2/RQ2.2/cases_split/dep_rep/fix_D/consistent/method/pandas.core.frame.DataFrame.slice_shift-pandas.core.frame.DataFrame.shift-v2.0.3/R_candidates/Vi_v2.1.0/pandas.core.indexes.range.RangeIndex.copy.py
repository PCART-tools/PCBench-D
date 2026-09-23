    @doc(Index.copy)
    def copy(self, name: Hashable | None = None, deep: bool = False) -> Self:
        name = self._validate_names(name=name, deep=deep)[0]
        new_index = self._rename(name=name)
        return new_index
