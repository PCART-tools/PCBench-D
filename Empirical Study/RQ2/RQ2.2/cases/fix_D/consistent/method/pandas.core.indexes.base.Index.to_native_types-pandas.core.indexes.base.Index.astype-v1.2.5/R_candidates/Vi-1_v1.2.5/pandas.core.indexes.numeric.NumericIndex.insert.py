    @doc(Index.insert)
    def insert(self, loc: int, item):
        try:
            item = self._validate_fill_value(item)
        except TypeError:
            return self.astype(object).insert(loc, item)

        return super().insert(loc, item)
