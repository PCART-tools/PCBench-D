    def __array_finalize__(self, obj):
        """
        Gets called after any ufunc or other array operations, necessary
        to pass on the index.
        """
        self.sp_index = getattr(obj, 'sp_index', None)
        self._fill_value = getattr(obj, 'fill_value', None)
