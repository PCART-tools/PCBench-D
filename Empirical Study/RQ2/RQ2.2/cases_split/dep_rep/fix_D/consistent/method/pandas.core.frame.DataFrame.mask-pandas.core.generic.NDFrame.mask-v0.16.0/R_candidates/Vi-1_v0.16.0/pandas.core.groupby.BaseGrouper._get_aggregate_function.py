    def _get_aggregate_function(self, how, values):

        dtype_str = values.dtype.name

        def get_func(fname):
            # find the function, or use the object function, or return a
            # generic
            for dt in [dtype_str, 'object']:
                f = getattr(_algos, "%s_%s" % (fname, dtype_str), None)
                if f is not None:
                    return f

            if dtype_str == 'float64':
                return getattr(_algos, fname, None)

        ftype = self._cython_functions[how]

        if isinstance(ftype, dict):
            func = afunc = get_func(ftype['name'])

            # a sub-function
            f = ftype.get('f')
            if f is not None:

                def wrapper(*args, **kwargs):
                    return f(afunc, *args, **kwargs)

                # need to curry our sub-function
                func = wrapper

        else:
            func = get_func(ftype)

        if func is None:
            raise NotImplementedError("function is not implemented for this"
                                      "dtype: [how->%s,dtype->%s]" %
                                      (how, dtype_str))
        return func, dtype_str
