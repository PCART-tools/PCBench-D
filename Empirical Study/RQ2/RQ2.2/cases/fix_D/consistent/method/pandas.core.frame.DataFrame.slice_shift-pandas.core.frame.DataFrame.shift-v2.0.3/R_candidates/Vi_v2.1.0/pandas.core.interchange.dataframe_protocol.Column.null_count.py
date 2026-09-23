    @property
    @abstractmethod
    def null_count(self) -> int | None:
        """
        Number of null elements, if known.

        Note: Arrow uses -1 to indicate "unknown", but None seems cleaner.
        """
