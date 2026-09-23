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
        subset : label, array-like, IndexSlice, optional
            A valid 2d input to `DataFrame.loc[<subset>]`, or, in the case of a 1d input
            or single key, to `DataFrame.loc[:, <subset>]` where the columns are
            prioritised, to limit ``data`` to *before* applying the function.
        color : str, default 'yellow'
            Background color to use for highlighting.
        axis : {0 or 'index', 1 or 'columns', None}, default 0
            Apply to each column (``axis=0`` or ``'index'``), to each row
            (``axis=1`` or ``'columns'``), or to the entire DataFrame at once
            with ``axis=None``.
        props : str, default None
            CSS properties to use for highlighting. If ``props`` is given, ``color``
            is not used.

            .. versionadded:: 1.3.0

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.highlight_null: Highlight missing values with a style.
        Styler.highlight_min: Highlight the minimum with a style.
        Styler.highlight_between: Highlight a defined range with a style.
        Styler.highlight_quantile: Highlight values defined by a quantile with a style.
        """

        if props is None:
            props = f"background-color: {color};"
        # error: Argument 1 to "apply" of "Styler" has incompatible type
        # "Callable[[FrameOrSeries, str], ndarray]"; expected "Callable[..., Styler]"
        return self.apply(
            partial(_highlight_value, op="max"),  # type: ignore[arg-type]
            axis=axis,
            subset=subset,
            props=props,
        )
