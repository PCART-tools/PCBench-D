    def _set_categories(self, categories):
        """ Sets new categories """
        categories = self._validate_categories(categories)
        if not self._categories is None and len(categories) != len(self._categories):
            raise ValueError("new categories need to have the same number of items than the old "
                             "categories!")
        self._categories = categories
