    @abc.abstractmethod
    def _load(self) -> StubHandler | None:
        """(Hook) Find actual image loader."""
        pass
