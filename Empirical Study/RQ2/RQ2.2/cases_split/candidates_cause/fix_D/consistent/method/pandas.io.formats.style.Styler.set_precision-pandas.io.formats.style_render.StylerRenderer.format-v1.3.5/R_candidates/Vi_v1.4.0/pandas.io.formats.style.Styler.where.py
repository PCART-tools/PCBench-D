    @Substitution(subset=subset)
    def where(
        self,
        cond: Callable,
        value: str,
        other: str | None = None,
        subset: Subset | None = None,
        **kwargs,
    ) -> Styler:
        """
        Apply CSS-styles based on a conditional function elementwise.

        .. deprecated:: 1.3.0

        Updates the HTML representation with a style which is
        selected in accordance with the return value of a function.

        Parameters
        ----------
        cond : callable
            ``cond`` should take a scalar, and optional keyword arguments, and return
            a boolean.
        value : str
            Applied when ``cond`` returns true.
        other : str
            Applied when ``cond`` returns false.
        %(subset)s
        **kwargs : dict
            Pass along to ``cond``.

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.applymap: Apply a CSS-styling function elementwise.
        Styler.apply: Apply a CSS-styling function column-wise, row-wise, or table-wise.

        Notes
        -----
        This method is deprecated.

        This method is a convenience wrapper for :meth:`Styler.applymap`, which we
        recommend using instead.

        The example:

        >>> df = pd.DataFrame([[1, 2], [3, 4]])
        >>> def cond(v, limit=4):
        ...     return v > 1 and v != limit
        >>> df.style.where(cond, value='color:green;', other='color:red;')
        ...  # doctest: +SKIP

        should be refactored to:

        >>> def style_func(v, value, other, limit=4):
        ...     cond = v > 1 and v != limit
        ...     return value if cond else other
        >>> df.style.applymap(style_func, value='color:green;', other='color:red;')
        ...  # doctest: +SKIP
        """
        warnings.warn(
            "this method is deprecated in favour of `Styler.applymap()`",
            FutureWarning,
            stacklevel=find_stack_level(),
        )

        if other is None:
            other = ""

        return self.applymap(
            lambda val: value if cond(val, **kwargs) else other,
            subset=subset,
        )
