    @doc(Index.unique)
    def unique(self, level=None):
        if level is not None:
            self._validate_index_level(level)
        result = self._values.unique()
        # Use _simple_new instead of _shallow_copy to ensure we keep dtype
        #  of result, not self.
        return type(self)._simple_new(result, name=self.name)
