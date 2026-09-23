    @property
    def _has_complex_internals(self):
        """
        Indicates if an index is not directly backed by a numpy array
        """
        # used to avoid libreduction code paths, which raise or require conversion
        return False
