    def __array_wrap__(self, result, context=None):
        """
        Gets called after a ufunc
        """
        return self._shallow_copy(result)
