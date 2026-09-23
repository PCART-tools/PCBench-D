    @property
    def name(self) -> str:  # type: ignore[override]
        """
        A string identifying the data type.
        """
        return f"{str(self.pyarrow_dtype)}[{self.storage}]"
