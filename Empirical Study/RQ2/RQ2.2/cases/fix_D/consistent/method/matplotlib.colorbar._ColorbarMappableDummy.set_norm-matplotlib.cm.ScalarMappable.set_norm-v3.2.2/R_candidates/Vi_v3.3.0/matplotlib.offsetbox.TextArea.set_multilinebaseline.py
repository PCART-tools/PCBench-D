    def set_multilinebaseline(self, t):
        """
        Set multilinebaseline.

        If True, baseline for multiline text is adjusted so that it is
        (approximately) center-aligned with single-line text.
        """
        self._multilinebaseline = t
        self.stale = True
