    def _finalize(
        self, categories, ordered: OrderedType, fastpath: bool = False
    ) -> None:

        if ordered is not None and ordered is not ordered_sentinel:
            self.validate_ordered(ordered)

        if categories is not None:
            categories = self.validate_categories(categories, fastpath=fastpath)

        self._categories = categories
        self._ordered = ordered if ordered is not ordered_sentinel else None
        self._ordered_from_sentinel = ordered is ordered_sentinel
