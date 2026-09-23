    @Appender(_shared_docs["items"] % "Yields\n        ------")
    def items(self):
        if self.columns.is_unique and hasattr(self, "_item_cache"):
            for k in self.columns:
                yield k, self._get_item_cache(k)
        else:
            for i, k in enumerate(self.columns):
                yield k, self._ixs(i, axis=1)
