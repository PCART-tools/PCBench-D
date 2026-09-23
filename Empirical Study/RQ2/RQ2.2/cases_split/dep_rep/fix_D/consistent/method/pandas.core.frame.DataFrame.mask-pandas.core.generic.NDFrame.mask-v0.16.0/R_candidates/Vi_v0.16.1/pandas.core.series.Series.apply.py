    def apply(self, func, convert_dtype=True, args=(), **kwds):
        """
        Invoke function on values of Series. Can be ufunc (a NumPy function
        that applies to the entire Series) or a Python function that only works
        on single values

        Parameters
        ----------
        func : function
        convert_dtype : boolean, default True
            Try to find better dtype for elementwise function results. If
            False, leave as dtype=object
        args : tuple
            Positional arguments to pass to function in addition to the value
        Additional keyword arguments will be passed as keywords to the function

        See also
        --------
        Series.map: For element-wise operations

        Returns
        -------
        y : Series or DataFrame if func returns a Series
        """
        if len(self) == 0:
            return self._constructor(dtype=self.dtype,
                                     index=self.index).__finalize__(self)

        if kwds or args and not isinstance(func, np.ufunc):
            f = lambda x: func(x, *args, **kwds)
        else:
            f = func

        if isinstance(f, np.ufunc):
            return f(self)

        values = _values_from_object(self)
        if com.is_datetime64_dtype(values.dtype):
            values = lib.map_infer(values, lib.Timestamp)

        mapped = lib.map_infer(values, f, convert=convert_dtype)
        if len(mapped) and isinstance(mapped[0], Series):
            from pandas.core.frame import DataFrame
            return DataFrame(mapped.tolist(), index=self.index)
        else:
            return self._constructor(mapped,
                                     index=self.index).__finalize__(self)
