    @doc(Index.fillna)
    def fillna(self, value, downcast=None):
        value = self._require_scalar(value)
        try:
            cat = self._data.fillna(value)
        except (ValueError, TypeError):
            # invalid fill_value
            if not self.isna().any():
                # nothing to fill, we can get away without casting
                return self.copy()
            return self.astype(object).fillna(value, downcast=downcast)

        return type(self)._simple_new(cat, name=self.name)
