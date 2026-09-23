    def _finalize(self, categories, ordered: Ordered, fastpath: bool = False) -> None:
        if ordered is not None:
            self.validate_ordered(ordered)

        if categories is not None:
            categories = self.validate_categories(categories, fastpath=fastpath)

        self._categories = categories
        self._ordered = ordered
