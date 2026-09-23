    @property
    def _has_complex_internals(self):
        # used to avoid libreduction code paths, which raise or require conversion
        return True
