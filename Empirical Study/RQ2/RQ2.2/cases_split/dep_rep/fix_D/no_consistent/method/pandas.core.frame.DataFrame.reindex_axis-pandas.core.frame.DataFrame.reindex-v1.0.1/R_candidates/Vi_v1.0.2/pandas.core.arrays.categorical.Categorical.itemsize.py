    @cache_readonly
    def itemsize(self) -> int:
        """
        return the size of a single category
        """
        return self.categories.itemsize
