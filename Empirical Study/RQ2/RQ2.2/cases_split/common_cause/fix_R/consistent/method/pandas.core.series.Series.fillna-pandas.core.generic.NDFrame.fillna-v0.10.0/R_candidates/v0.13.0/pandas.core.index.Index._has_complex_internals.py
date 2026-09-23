    @property
    def _has_complex_internals(self):
        # to disable groupby tricks in MultiIndex
        return False
