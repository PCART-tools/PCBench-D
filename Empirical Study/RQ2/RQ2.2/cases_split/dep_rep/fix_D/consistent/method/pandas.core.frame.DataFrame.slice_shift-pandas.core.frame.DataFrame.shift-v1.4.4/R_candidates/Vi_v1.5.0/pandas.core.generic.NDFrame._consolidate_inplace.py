    @final
    def _consolidate_inplace(self) -> None:
        """Consolidate data in place and return None"""

        def f():
            self._mgr = self._mgr.consolidate()

        self._protect_consolidate(f)
