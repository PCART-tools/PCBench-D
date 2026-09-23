    def _load(self) -> StubHandler | None:
        """(Hook) Find actual image loader."""
        msg = "StubImageFile subclass must implement _load"
        raise NotImplementedError(msg)
