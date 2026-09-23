    def _check_compatible_with(self, other) -> None:
        if other is NaT:
            return
        self._assert_tzawareness_compat(other)
