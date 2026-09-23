    def __getitem__(self, key):
        # per GH 23566
        if isinstance(key, tuple) and len(key) > 1:
            # if len == 1, then it becomes a SeriesGroupBy and this is actually
            # valid syntax, so don't raise warning
            warnings.warn(
                "Indexing with multiple keys (implicitly converted to a tuple "
                "of keys) will be deprecated, use a list instead.",
                FutureWarning,
                stacklevel=2,
            )
        return super().__getitem__(key)
