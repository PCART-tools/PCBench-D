    def __deepcopy__(self, memo: None = None) -> LazyFrame:
        return self.clone()
