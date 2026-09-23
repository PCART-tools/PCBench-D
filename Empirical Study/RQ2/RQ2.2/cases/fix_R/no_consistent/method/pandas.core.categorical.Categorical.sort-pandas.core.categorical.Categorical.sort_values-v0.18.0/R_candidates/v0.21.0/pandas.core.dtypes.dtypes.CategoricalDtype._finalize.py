    def _finalize(self, categories, ordered, fastpath=False):

        if ordered is None:
            ordered = False
        else:
            self._validate_ordered(ordered)

        if categories is not None:
            categories = self._validate_categories(categories,
                                                   fastpath=fastpath)

        self._categories = categories
        self._ordered = ordered
