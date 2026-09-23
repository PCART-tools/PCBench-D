    @doc(Index.copy)
    def copy(self, name: Hashable = None, deep: bool = False):
        name = self._validate_names(name=name, deep=deep)[0]
        new_index = self._rename(name=name)
        return new_index
