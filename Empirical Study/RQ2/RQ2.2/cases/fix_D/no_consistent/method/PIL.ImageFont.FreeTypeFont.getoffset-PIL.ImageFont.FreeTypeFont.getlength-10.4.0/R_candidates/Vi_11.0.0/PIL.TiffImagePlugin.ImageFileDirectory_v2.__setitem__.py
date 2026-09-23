    def __setitem__(self, tag: int, value: Any) -> None:
        self._setitem(tag, value, self.legacy_api)
