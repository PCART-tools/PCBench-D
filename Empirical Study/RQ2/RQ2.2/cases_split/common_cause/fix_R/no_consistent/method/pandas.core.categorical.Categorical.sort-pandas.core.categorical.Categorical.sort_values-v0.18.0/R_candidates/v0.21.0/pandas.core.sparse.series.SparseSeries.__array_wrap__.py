    def __array_wrap__(self, result, context=None):
        """
        Gets called prior to a ufunc (and after)

        See SparseArray.__array_wrap__ for detail.
        """
        if isinstance(context, tuple) and len(context) == 3:
            ufunc, args, domain = context
            args = [getattr(a, 'fill_value', a) for a in args]
            with np.errstate(all='ignore'):
                fill_value = ufunc(self.fill_value, *args[1:])
        else:
            fill_value = self.fill_value

        return self._constructor(result, index=self.index,
                                 sparse_index=self.sp_index,
                                 fill_value=fill_value,
                                 copy=False).__finalize__(self)
