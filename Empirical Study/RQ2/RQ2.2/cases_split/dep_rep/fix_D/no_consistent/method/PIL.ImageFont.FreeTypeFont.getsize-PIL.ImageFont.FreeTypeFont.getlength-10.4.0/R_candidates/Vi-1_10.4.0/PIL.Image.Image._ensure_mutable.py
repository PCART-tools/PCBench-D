    def _ensure_mutable(self) -> None:
        if self.readonly:
            self._copy()
        else:
            self.load()
