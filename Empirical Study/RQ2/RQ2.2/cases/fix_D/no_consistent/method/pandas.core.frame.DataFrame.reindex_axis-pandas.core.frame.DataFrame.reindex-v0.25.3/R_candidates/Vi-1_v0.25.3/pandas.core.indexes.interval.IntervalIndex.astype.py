    @Appender(_index_shared_docs["astype"])
    def astype(self, dtype, copy=True):
        with rewrite_exception("IntervalArray", self.__class__.__name__):
            new_values = self.values.astype(dtype, copy=copy)
        if is_interval_dtype(new_values):
            return self._shallow_copy(new_values.left, new_values.right)
        return super().astype(dtype, copy=copy)
