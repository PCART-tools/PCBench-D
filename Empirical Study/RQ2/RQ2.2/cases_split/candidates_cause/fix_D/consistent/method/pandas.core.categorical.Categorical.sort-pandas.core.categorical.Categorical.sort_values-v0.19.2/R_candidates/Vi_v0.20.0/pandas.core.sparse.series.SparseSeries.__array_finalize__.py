    def __array_finalize__(self, obj):
        """
        Gets called after any ufunc or other array operations, necessary
        to pass on the index.
        """
        self.name = getattr(obj, 'name', None)
        self.fill_value = getattr(obj, 'fill_value', None)
