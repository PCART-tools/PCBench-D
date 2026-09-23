    @property
    def has_index_names(self) -> bool:
        return _has_names(self.frame.index)
