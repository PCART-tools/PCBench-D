    @cache_readonly
    def _ilevel(self) -> int | None:
        """
        If necessary, converted index level name to index level position.
        """
        level = self.level
        if level is None:
            return None
        if not isinstance(level, int):
            index = self._index
            if level not in index.names:
                raise AssertionError(f"Level {level} not in index")
            return index.names.index(level)
        return level
