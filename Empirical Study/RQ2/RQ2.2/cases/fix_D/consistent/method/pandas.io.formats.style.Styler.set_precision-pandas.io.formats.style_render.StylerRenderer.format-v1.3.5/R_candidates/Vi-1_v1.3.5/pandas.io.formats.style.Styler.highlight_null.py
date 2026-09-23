    def highlight_null(
        self,
        null_color: str = "red",
        subset: Subset | None = None,
        props: str | None = None,
    ) -> Styler:
        """
        Highlight missing values with a style.

        Parameters
        ----------
        null_color : str, default 'red'
        subset : label, array-like, IndexSlice, optional
            A valid 2d input to `DataFrame.loc[<subset>]`, or, in the case of a 1d input
            or single key, to `DataFrame.loc[:, <subset>]` where the columns are
            prioritised, to limit ``data`` to *before* applying the function.

            .. versionadded:: 1.1.0

        props : str, default None
            CSS properties to use for highlighting. If ``props`` is given, ``color``
            is not used.

            .. versionadded:: 1.3.0

        Returns
        -------
        self : Styler

        See Also
        --------
        Styler.highlight_max: Highlight the maximum with a style.
        Styler.highlight_min: Highlight the minimum with a style.
        Styler.highlight_between: Highlight a defined range with a style.
        Styler.highlight_quantile: Highlight values defined by a quantile with a style.
        """

        def f(data: DataFrame, props: str) -> np.ndarray:
            return np.where(pd.isna(data).to_numpy(), props, "")

        if props is None:
            props = f"background-color: {null_color};"
        # error: Argument 1 to "apply" of "Styler" has incompatible type
        # "Callable[[DataFrame, str], ndarray]"; expected "Callable[..., Styler]"
        return self.apply(
            f, axis=None, subset=subset, props=props  # type: ignore[arg-type]
        )
