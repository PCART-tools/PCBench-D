    @property
    @unstable()
    def plot(self) -> hvPlotTabularPolars:
        """
        Create a plot namespace.

        .. warning::
            This functionality is currently considered **unstable**. It may be
            changed at any point without it being considered a breaking change.

        Polars does not implement plotting logic itself, but instead defers to
        hvplot. Please see the `hvplot reference gallery <https://hvplot.holoviz.org/reference/index.html>`_
        for more information and documentation.

        Examples
        --------
        Scatter plot:

        >>> df = pl.DataFrame(
        ...     {
        ...         "length": [1, 4, 6],
        ...         "width": [4, 5, 6],
        ...         "species": ["setosa", "setosa", "versicolor"],
        ...     }
        ... )
        >>> df.plot.scatter(x="length", y="width", by="species")  # doctest: +SKIP

        Line plot:

        >>> from datetime import date
        >>> df = pl.DataFrame(
        ...     {
        ...         "date": [date(2020, 1, 2), date(2020, 1, 3), date(2020, 1, 4)],
        ...         "stock_1": [1, 4, 6],
        ...         "stock_2": [1, 5, 2],
        ...     }
        ... )
        >>> df.plot.line(x="date", y=["stock_1", "stock_2"])  # doctest: +SKIP

        For more info on what you can pass, you can use ``hvplot.help``:

        >>> import hvplot  # doctest: +SKIP
        >>> hvplot.help("scatter")  # doctest: +SKIP
        """
        if not _HVPLOT_AVAILABLE or parse_version(hvplot.__version__) < parse_version(
            "0.9.1"
        ):
            msg = "hvplot>=0.9.1 is required for `.plot`"
            raise ModuleUpgradeRequiredError(msg)
        hvplot.post_patch()
        return hvplot.plotting.core.hvPlotTabularPolars(self)
