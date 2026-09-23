    def __getitem__(self, item: int | range | slice) -> LazyFrame:
        if not isinstance(item, slice):
            raise TypeError(
                "'LazyFrame' object is not subscriptable (aside from slicing)"
                "\n\nUse `select()` or `filter()` instead."
            )
        return LazyPolarsSlice(self).apply(item)
