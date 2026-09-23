    @final
    def _dir_additions(self) -> set[str]:
        return self.obj._dir_additions() | self._apply_allowlist
