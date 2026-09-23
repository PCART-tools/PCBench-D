    @property
    @abstractmethod
    def metadata(self) -> dict[str, Any]:
        """
        The metadata for the column. See `DataFrame.metadata` for more details.
        """
        pass
