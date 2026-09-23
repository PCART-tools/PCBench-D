    def _set_levels(self, levels):
        """ set new levels (deprecated, use "categories") """
        warn("Assigning to 'levels' is deprecated, use 'categories'", FutureWarning)
        self.categories = levels
