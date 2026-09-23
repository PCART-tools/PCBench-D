    @cache_readonly
    def _on(self) -> Index:
        if self.on is None:
            if self.axis == 0:
                return self.obj.index
            else:
                # i.e. self.axis == 1
                return self.obj.columns
        elif isinstance(self.on, Index):
            return self.on
        elif isinstance(self.obj, ABCDataFrame) and self.on in self.obj.columns:
            return Index(self.obj[self.on])
        else:
            raise ValueError(
                f"invalid on specified as {self.on}, "
                "must be a column (of DataFrame), an Index "
                "or None"
            )
