    @Substitution(subset=subset, props=props)
    def highlight_min(
        self,
        subset: Subset | None = None,
        color: str = "yellow",
        axis: Axis | None = 0,
        props: str | None = None,
    ) -> Styler:
        """
        Highlight the minimum with a style.

        Parameters
        ----------
        %(subset)s
        color : str, default 'yellow'
            Background color to use for highlighting.
        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Apply to each column (``axis=0`` or ``'index'``), to each row
            (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
            with ``axis=None``.
        %(props)s
            .. versionadded:: 1.3.0

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.highlight_null: Highlight missing values with a style.
        Styler.highlight_max: Highlight the maximum with a style.
        Styler.highlight_between: Highlight a defined range with a style.
        Styler.highlight_quantile: Highlight values defined by a quantile with a style.
        """

        if props is None:
            props = f"background-color: {color};"
        return self.apply(
            partial(_highlight_value, op="min"),
            axis=axis,
            subset=subset,
            props=props,
        )
