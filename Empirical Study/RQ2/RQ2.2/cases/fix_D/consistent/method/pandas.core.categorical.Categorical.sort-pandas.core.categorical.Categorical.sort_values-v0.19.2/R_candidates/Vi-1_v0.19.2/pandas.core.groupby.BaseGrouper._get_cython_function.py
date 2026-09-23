    def _get_cython_function(self, kind, how, values, is_numeric):

        dtype_str = values.dtype.name

        def get_func(fname):
            # see if there is a fused-type version of function
            # only valid for numeric
            f = getattr(_algos, fname, None)
            if f is not None and is_numeric:
                return f

            # otherwise find dtype-specific version, falling back to object
            for dt in [dtype_str, 'object']:
                f = getattr(_algos, "%s_%s" % (fname, dtype_str), None)
                if f is not None:
                    return f

        ftype = self._cython_functions[kind][how]

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
