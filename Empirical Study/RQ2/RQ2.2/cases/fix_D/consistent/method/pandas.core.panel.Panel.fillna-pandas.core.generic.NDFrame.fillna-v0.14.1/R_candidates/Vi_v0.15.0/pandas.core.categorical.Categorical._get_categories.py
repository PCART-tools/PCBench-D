    def _get_categories(self):
        """ Gets the categories """
        # categories is an Index, which is immutable -> no need to copy
        return self._categories
