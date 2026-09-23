    @property
    def group_index(self) -> Index:
        if self._group_index is None:
            self._make_codes()
        assert self._group_index is not None
        return self._group_index
