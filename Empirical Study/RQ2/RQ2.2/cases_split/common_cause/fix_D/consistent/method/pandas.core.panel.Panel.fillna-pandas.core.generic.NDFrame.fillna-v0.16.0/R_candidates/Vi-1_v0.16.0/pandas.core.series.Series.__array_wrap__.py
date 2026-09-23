    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc
        """
        return self._constructor(result, index=self.index,
                                 copy=False).__finalize__(self)
