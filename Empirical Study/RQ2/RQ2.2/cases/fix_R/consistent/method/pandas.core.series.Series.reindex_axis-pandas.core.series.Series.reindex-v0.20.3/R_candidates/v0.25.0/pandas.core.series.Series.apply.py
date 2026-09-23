    def apply(self, func, convert_dtype=True, args=(), **kwds):
        """
        Invoke function on values of Series.

        Can be ufunc (a NumPy function that applies to the entire Series)
        or a Python function that only works on single values.

        Parameters
        ----------
        func : function
            Python function or NumPy ufunc to apply.
        convert_dtype : bool, default True
            Try to find better dtype for elementwise function results. If
            False, leave as dtype=object.
        args : tuple
            Positional arguments passed to func after the series value.
        **kwds
            Additional keyword arguments passed to func.

        Returns
        -------
        Series or DataFrame
            If func returns a Series object the result will be a DataFrame.

        See Also
        --------
        Series.map: For element-wise operations.
        Series.agg: Only perform aggregating type operations.
        Series.transform: Only perform transforming type operations.

        Examples
        --------
        Create a series with typical summer temperatures for each city.

        >>> s = pd.Series([20, 21, 12],
        ...               index=['London', 'New York', 'Helsinki'])
        >>> s
        London      20
        New York    21
        Helsinki    12
        dtype: int64

        Square the values by defining a function and passing it as an
        argument to ``apply()``.

        >>> def square(x):
        ...     return x ** 2
        >>> s.apply(square)
        London      400
        New York    441
        Helsinki    144
        dtype: int64

        Square the values by passing an anonymous function as an
        argument to ``apply()``.

        >>> s.apply(lambda x: x ** 2)
        London      400
        New York    441
        Helsinki    144
        dtype: int64

        Define a custom function that needs additional positional
        arguments and pass these additional arguments using the
        ``args`` keyword.

        >>> def subtract_custom_value(x, custom_value):
        ...     return x - custom_value

        >>> s.apply(subtract_custom_value, args=(5,))
        London      15
        New York    16
        Helsinki     7
        dtype: int64

        Define a custom function that takes keyword arguments
        and pass these arguments to ``apply``.

        >>> def add_custom_values(x, **kwargs):
        ...     for month in kwargs:
        ...         x += kwargs[month]
        ...     return x

        >>> s.apply(add_custom_values, june=30, july=20, august=25)
        London      95
        New York    96
        Helsinki    87
        dtype: int64

        Use a function from the Numpy library.

        >>> s.apply(np.log)
        London      2.995732
        New York    3.044522
        Helsinki    2.484907
        dtype: float64
        """
        if len(self) == 0:
            return self._constructor(dtype=self.dtype, index=self.index).__finalize__(
                self
            )

        # dispatch to agg
        if isinstance(func, (list, dict)):
            return self.aggregate(func, *args, **kwds)

        # if we are a string, try to dispatch
        if isinstance(func, str):
            return self._try_aggregate_string_function(func, *args, **kwds)

        # handle ufuncs and lambdas
        if kwds or args and not isinstance(func, np.ufunc):

            def f(x):
                return func(x, *args, **kwds)

        else:
            f = func

        with np.errstate(all="ignore"):
            if isinstance(f, np.ufunc):
                return f(self)

            # row-wise access
            if is_extension_type(self.dtype):
                mapped = self._values.map(f)
            else:
                values = self.astype(object).values
                mapped = lib.map_infer(values, f, convert=convert_dtype)

        if len(mapped) and isinstance(mapped[0], Series):
            # GH 25959 use pd.array instead of tolist
            # so extension arrays can be used
            return self._constructor_expanddim(pd.array(mapped), index=self.index)
        else:
            return self._constructor(mapped, index=self.index).__finalize__(self)
