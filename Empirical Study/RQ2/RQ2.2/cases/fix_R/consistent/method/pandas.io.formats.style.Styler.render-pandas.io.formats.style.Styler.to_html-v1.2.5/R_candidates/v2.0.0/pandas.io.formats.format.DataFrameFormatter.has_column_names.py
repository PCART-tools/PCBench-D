    @property
    def has_column_names(self) -> bool:
        return _has_names(self.frame.columns)
