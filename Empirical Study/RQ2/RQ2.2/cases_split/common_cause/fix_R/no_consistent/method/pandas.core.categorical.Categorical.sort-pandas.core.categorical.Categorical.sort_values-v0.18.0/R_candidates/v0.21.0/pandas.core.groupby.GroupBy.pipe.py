    def pipe(self, func, *args, **kwargs):
        """ Apply a function with arguments to this GroupBy object,

        .. versionadded:: 0.21.0

        Parameters
        ----------
        func : callable or tuple of (callable, string)
            Function to apply to this GroupBy object or, alternatively, a
            ``(callable, data_keyword)`` tuple where ``data_keyword`` is a
            string indicating the keyword of ``callable`` that expects the
            GroupBy object.
        args : iterable, optional
               positional arguments passed into ``func``.
        kwargs : dict, optional
                 a dictionary of keyword arguments passed into ``func``.

        Returns
        -------
        object : the return type of ``func``.

        Notes
        -----
        Use ``.pipe`` when chaining together functions that expect
        Series, DataFrames or GroupBy objects. Instead of writing

        >>> f(g(h(df.groupby('group')), arg1=a), arg2=b, arg3=c)

        You can write

        >>> (df
        ...    .groupby('group')
        ...    .pipe(f, arg1)
        ...    .pipe(g, arg2)
        ...    .pipe(h, arg3))

        See more `here
        <http://pandas.pydata.org/pandas-docs/stable/groupby.html#pipe>`_

        See Also
        --------
        pandas.Series.pipe : Apply a function with arguments to a series
        pandas.DataFrame.pipe: Apply a function with arguments to a dataframe
        apply : Apply function to each group instead of to the
            full GroupBy object.
        """
        return _pipe(self, func, *args, **kwargs)
