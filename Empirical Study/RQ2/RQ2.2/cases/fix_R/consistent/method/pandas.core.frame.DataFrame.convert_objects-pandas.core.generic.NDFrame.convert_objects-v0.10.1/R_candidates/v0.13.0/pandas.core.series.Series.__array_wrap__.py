    def __array_wrap__(self, result):
        """
        Gets called prior to a ufunc (and after)
        """
        return self._constructor(result, index=self.index,
                                 copy=False).__finalize__(self)
