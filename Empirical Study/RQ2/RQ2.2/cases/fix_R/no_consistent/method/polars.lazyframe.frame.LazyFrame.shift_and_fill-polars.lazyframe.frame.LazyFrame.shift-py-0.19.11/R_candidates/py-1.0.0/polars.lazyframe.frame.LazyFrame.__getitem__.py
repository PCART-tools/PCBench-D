    def __getitem__(self, item: int | range | slice) -> LazyFrame:
        if not isinstance(item, slice):
            msg = (
                "'LazyFrame' object is not subscriptable (aside from slicing)"
                "\n\nUse `select()` or `filter()` instead."
            )
            raise TypeError(msg)
        return LazyPolarsSlice(self).apply(item)
