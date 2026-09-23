    def drop_duplicates(self, *, keep: DropKeep = "first"):
        duplicated = self._duplicated(keep=keep)
        # error: Value of type "IndexOpsMixin" is not indexable
        return self[~duplicated]  # type: ignore[index]
