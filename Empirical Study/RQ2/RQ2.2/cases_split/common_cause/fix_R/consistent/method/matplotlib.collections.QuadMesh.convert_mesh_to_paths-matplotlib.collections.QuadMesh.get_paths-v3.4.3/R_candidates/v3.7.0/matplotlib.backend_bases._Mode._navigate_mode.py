    @property
    def _navigate_mode(self):
        return self.name if self is not _Mode.NONE else None
