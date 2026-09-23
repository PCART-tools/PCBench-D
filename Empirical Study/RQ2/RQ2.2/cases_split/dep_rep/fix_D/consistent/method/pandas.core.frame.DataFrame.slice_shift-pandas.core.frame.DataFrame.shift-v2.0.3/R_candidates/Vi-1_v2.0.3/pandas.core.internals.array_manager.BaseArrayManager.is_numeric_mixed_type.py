    @property
    def is_numeric_mixed_type(self) -> bool:
        return all(is_numeric_dtype(t) for t in self.get_dtypes())
