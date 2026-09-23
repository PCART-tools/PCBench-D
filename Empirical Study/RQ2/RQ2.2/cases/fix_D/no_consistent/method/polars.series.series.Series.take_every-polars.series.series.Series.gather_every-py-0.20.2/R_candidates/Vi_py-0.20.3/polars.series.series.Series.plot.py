    @property
    def plot(self) -> Any:
        """
        Create a plot namespace.

        Polars does not implement plotting logic itself, but instead defers to
        hvplot. Please see the `hvplot reference gallery <https://hvplot.holoviz.org/reference/index.html>`_
        for more information and documentation.

        Examples
        --------
        Histogram:

        >>> s = pl.Series([1, 4, 2])
        >>> s.plot.hist()  # doctest: +SKIP

        KDE plot (note: in addition to ``hvplot``, this one also requires ``scipy``):

        >>> s.plot.kde()  # doctest: +SKIP

        For more info on what you can pass, you can use ``hvplot.help``:

        >>> import hvplot  # doctest: +SKIP
        >>> hvplot.help("hist")  # doctest: +SKIP
        """
        if not _HVPLOT_AVAILABLE or parse_version(hvplot.__version__) < parse_version(
            "0.9.1"
        ):
            raise ModuleUpgradeRequired("hvplot>=0.9.1 is required for `.plot`")
        hvplot.post_patch()
        return hvplot.plotting.core.hvPlotTabularPolars(self)
