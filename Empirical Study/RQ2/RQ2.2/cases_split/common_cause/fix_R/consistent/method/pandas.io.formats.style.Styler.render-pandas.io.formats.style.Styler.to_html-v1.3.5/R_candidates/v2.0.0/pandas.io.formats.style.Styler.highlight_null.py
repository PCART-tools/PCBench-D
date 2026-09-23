    @Substitution(
        subset=subset_args,
        props=properties_args,
        color=coloring_args.format(default="red"),
    )
    def highlight_null(
        self,
        color: str = "red",
        subset: Subset | None = None,
        props: str | None = None,
    ) -> Styler:
        """
        Highlight missing values with a style.

        Parameters
        ----------
        %(color)s

            .. versionadded:: 1.5.0

        %(subset)s

            .. versionadded:: 1.1.0

        %(props)s

            .. versionadded:: 1.3.0

        Returns
        -------
        Styler

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
            props = f"background-color: {color};"
        return self.apply(f, axis=None, subset=subset, props=props)
