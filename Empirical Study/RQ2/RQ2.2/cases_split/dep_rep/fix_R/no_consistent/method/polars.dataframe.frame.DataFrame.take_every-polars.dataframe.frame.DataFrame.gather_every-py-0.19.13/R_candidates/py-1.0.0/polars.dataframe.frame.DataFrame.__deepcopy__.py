    def __deepcopy__(self, memo: None = None) -> DataFrame:
        return self.clone()
