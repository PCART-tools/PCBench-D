    @cache_readonly
    def itemsize(self):
        """ return the size of a single category """
        return self.categories.itemsize
