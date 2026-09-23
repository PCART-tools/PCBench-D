    @Substitution(
        subset=subset_args,
        color=coloring_args.format(default="yellow"),
        props=properties_args,
    )
    def highlight_max(
        self,
        subset: Subset | None = None,
        color: str = "yellow",
        axis: Axis | None = 0,
        props: str | None = None,
    ) -> Styler:
        """
        Highlight the maximum with a style.

        Parameters
        ----------
        %(subset)s
        %(color)s
        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Apply to each column (``axis=0`` or ``'index'``), to each row
            (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
            with ``axis=None``.
        %(props)s

            .. versionadded:: 1.3.0

        Returns
        -------
        Styler

        See Also
        --------
        Styler.highlight_null: Highlight missing values with a style.
        Styler.highlight_min: Highlight the minimum with a style.
        Styler.highlight_between: Highlight a defined range with a style.
        Styler.highlight_quantile: Highlight values defined by a quantile with a style.

        Examples
        --------
        >>> df = pd.DataFrame({'A': [2, 1], 'B': [3, 4]})
        >>> df.style.highlight_max(color='yellow')  # doctest: +SKIP

        Please see:
        `Table Visualization <../../user_guide/style.ipynb>`_ for more examples.
        """

        if props is None:
            props = f"background-color: {color};"
        return self.apply(
            partial(_highlight_value, op="max"),
            axis=axis,
            subset=subset,
            props=props,
        )
