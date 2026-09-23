    @cache_readonly
    def _on(self):

        if self.on is None:
            return self.obj.index
        elif isinstance(self.obj, ABCDataFrame) and self.on in self.obj.columns:
            from pandas import Index

            return Index(self.obj[self.on])
        else:
            raise ValueError(
                "invalid on specified as {0}, "
                "must be a column (if DataFrame) "
                "or None".format(self.on)
            )
