    @abstractmethod
    def select_columns(self, indices: Sequence[int]) -> DataFrame:
        """
        Create a new DataFrame by selecting a subset of columns by index.
        """
