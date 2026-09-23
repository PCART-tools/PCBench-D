    def _get_levels(self):
        """ Gets the levels (deprecated, use "categories") """
        warn("Accessing 'levels' is deprecated, use 'categories'", FutureWarning)
        return self.categories
