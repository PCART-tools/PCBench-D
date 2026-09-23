    def __array_wrap__(self, out_arr, context=None):
        """
        NumPy calls this method when ufunc is applied

        Parameters
        ----------

        out_arr : ndarray
            ufunc result (note that ufunc is only applied to sp_values)
        context : tuple of 3 elements (ufunc, signature, domain)
            for example, following is a context when np.sin is applied to
            SparseArray,

            (<ufunc 'sin'>, (SparseArray,), 0))

        See http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
        """
        if isinstance(context, tuple) and len(context) == 3:
            ufunc, args, domain = context
            # to apply ufunc only to fill_value (to avoid recursive call)
            args = [getattr(a, 'fill_value', a) for a in args]
            with np.errstate(all='ignore'):
                fill_value = ufunc(self.fill_value, *args[1:])
        else:
            fill_value = self.fill_value

        return self._simple_new(out_arr, sp_index=self.sp_index,
                                fill_value=fill_value)
