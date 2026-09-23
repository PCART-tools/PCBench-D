    def _consolidate_inplace(self) -> None:
        """Consolidate data in place and return None"""

        def f():
            self._data = self._data.consolidate()

        self._protect_consolidate(f)
