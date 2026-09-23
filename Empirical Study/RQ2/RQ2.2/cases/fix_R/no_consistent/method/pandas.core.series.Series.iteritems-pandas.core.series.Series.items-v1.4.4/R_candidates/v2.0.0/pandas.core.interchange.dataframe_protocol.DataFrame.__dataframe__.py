    @abstractmethod
    def __dataframe__(self, nan_as_null: bool = False, allow_copy: bool = True):
        """Construct a new interchange object, potentially changing the parameters."""
