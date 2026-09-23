    def __array_wrap__(self, result, copy=False):
        """
        Gets called prior to a ufunc (and after)
        """
        return self._constructor(result, index=self.index,
                                 copy=copy).__finalize__(self)
