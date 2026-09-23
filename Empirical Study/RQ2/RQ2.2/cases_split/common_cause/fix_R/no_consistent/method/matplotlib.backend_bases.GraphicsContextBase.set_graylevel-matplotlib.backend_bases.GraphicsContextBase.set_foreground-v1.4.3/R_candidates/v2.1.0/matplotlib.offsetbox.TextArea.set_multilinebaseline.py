    def set_multilinebaseline(self, t):
        """
        Set multilinebaseline .

        If True, baseline for multiline text is
        adjusted so that it is (approximatedly) center-aligned with
        singleline text.
        """
        self._multilinebaseline = t
        self.stale = True
