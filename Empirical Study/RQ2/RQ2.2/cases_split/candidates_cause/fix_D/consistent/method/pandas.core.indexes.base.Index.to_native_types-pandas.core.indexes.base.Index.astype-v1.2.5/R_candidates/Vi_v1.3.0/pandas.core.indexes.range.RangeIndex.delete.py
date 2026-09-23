    def delete(self, loc) -> Int64Index:  # type: ignore[override]
        return self._int64index.delete(loc)
