    @Appender(Index.astype.__doc__)
    def astype(self, dtype, copy: bool = True):
        with rewrite_exception("IntervalArray", type(self).__name__):
            new_values = self._values.astype(dtype, copy=copy)
        return Index(new_values, dtype=new_values.dtype, name=self.name)
