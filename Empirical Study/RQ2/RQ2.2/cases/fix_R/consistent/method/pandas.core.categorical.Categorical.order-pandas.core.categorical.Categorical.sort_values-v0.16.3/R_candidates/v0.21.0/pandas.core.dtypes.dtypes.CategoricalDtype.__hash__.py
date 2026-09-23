    def __hash__(self):
        # _hash_categories returns a uint64, so use the negative
        # space for when we have unknown categories to avoid a conflict
        if self.categories is None:
            if self.ordered:
                return -1
            else:
                return -2
        # We *do* want to include the real self.ordered here
        return int(self._hash_categories(self.categories, self.ordered))
