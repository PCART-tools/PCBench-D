    @property
    def _can_hold_na(self):
        # The default ExtensionArray._can_hold_na is True
        return self._holder._can_hold_na
