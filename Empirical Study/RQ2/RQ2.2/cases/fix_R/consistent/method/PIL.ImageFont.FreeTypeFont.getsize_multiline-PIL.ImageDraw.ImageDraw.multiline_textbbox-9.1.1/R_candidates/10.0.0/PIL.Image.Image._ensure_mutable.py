    def _ensure_mutable(self):
        if self.readonly:
            self._copy()
        else:
            self.load()
