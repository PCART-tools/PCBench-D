    def __array_wrap__(self, result, context=None):
        """
        Gets called prior to a ufunc (and after)

        See SparseArray.__array_wrap__ for detail.
        """
        result = self.values.__array_wrap__(result, context=context)
        return self._constructor(result, index=self.index,
                                 sparse_index=self.sp_index,
                                 fill_value=result.fill_value,
                                 copy=False).__finalize__(self)
