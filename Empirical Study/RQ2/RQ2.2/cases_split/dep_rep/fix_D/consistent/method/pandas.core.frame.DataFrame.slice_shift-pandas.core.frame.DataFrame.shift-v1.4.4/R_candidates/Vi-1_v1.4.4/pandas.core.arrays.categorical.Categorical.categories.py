    @categories.setter
    def categories(self, categories):
        new_dtype = CategoricalDtype(categories, ordered=self.ordered)
        if self.dtype.categories is not None and len(self.dtype.categories) != len(
            new_dtype.categories
        ):
            raise ValueError(
                "new categories need to have the same number of "
                "items as the old categories!"
            )
        super().__init__(self._ndarray, new_dtype)
