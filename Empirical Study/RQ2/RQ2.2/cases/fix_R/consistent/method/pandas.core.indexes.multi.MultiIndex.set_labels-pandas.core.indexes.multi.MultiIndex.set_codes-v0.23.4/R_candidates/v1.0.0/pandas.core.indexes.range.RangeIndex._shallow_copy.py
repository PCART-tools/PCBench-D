    @Appender(_index_shared_docs["_shallow_copy"])
    def _shallow_copy(self, values=None, **kwargs):
        if values is None:
            name = kwargs.get("name", self.name)
            return self._simple_new(self._range, name=name)
        else:
            kwargs.setdefault("name", self.name)
            return self._int64index._shallow_copy(values, **kwargs)
