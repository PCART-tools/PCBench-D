    @property
    def _has_complex_internals(self) -> bool:
        # used to avoid libreduction code paths, which raise or require conversion
        return False
