    @cache_readonly
    def _index_as_unique(self) -> bool:
        return not self.is_overlapping and self._engine._na_count < 2
