    def pipe(self, func: Callable, *args, **kwargs):
        """
        Apply ``func(self, *args, **kwargs)``, and return the result.

        Parameters
        ----------
        func : function
            Function to apply to the Styler.  Alternatively, a
            ``(callable, keyword)`` tuple where ``keyword`` is a string
            indicating the keyword of ``callable`` that expects the Styler.
        *args : optional
            Arguments passed to `func`.
        **kwargs : optional
            A dictionary of keyword arguments passed into ``func``.

        Returns
        -------
        object :
            The value returned by ``func``.

        See Also
        --------
        DataFrame.pipe : Analogous method for DataFrame.
        Styler.apply : Apply a CSS-styling function column-wise, row-wise, or
            table-wise.

        Notes
        -----
        Like :meth:`DataFrame.pipe`, this method can simplify the
        application of several user-defined functions to a styler.  Instead
        of writing:

        .. code-block:: python

            f(g(df.style.set_precision(3), arg1=a), arg2=b, arg3=c)

        users can write:

        .. code-block:: python

            (df.style.set_precision(3)
               .pipe(g, arg1=a)
               .pipe(f, arg2=b, arg3=c))

        In particular, this allows users to define functions that take a
        styler object, along with other parameters, and return the styler after
        making styling changes (such as calling :meth:`Styler.apply` or
        :meth:`Styler.set_properties`).  Using ``.pipe``, these user-defined
        style "transformations" can be interleaved with calls to the built-in
        Styler interface.

        Examples
        --------
        >>> def format_conversion(styler):
        ...     return (styler.set_properties(**{'text-align': 'right'})
        ...                   .format({'conversion': '{:.1%}'}))

        The user-defined ``format_conversion`` function above can be called
        within a sequence of other style modifications:

        >>> df = pd.DataFrame({'trial': list(range(5)),
        ...                    'conversion': [0.75, 0.85, np.nan, 0.7, 0.72]})
        >>> (df.style
        ...    .highlight_min(subset=['conversion'], color='yellow')
        ...    .pipe(format_conversion)
        ...    .set_caption("Results with minimum conversion highlighted."))
        ...  # doctest: +SKIP

        .. figure:: ../../_static/style/df_pipe.png
        """
        return com.pipe(self, func, *args, **kwargs)
