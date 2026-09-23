    @abstractmethod
    def select_columns_by_name(self, names: Sequence[str]) -> DataFrame:
        """
        Create a new DataFrame by selecting a subset of columns by name.
        """
