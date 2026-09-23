    def _load(self):
        """(Hook) Find actual image loader."""
        msg = "StubImageFile subclass must implement _load"
        raise NotImplementedError(msg)
