    @property
    @unstable()
    def style(self) -> GT:
        """
        Create a Great Table for styling.

        .. warning::
            This functionality is currently considered **unstable**. It may be
            changed at any point without it being considered a breaking change.

        Polars does not implement styling logic itself, but instead defers to
        the Great Tables package. Please see the `Great Tables reference <https://posit-dev.github.io/great-tables/reference/>`_
        for more information and documentation.

        Examples
        --------
        Import some styling helpers, and create example data:

        >>> import polars.selectors as cs
        >>> from great_tables import loc, style
        >>> df = pl.DataFrame(
        ...     {
        ...         "site_id": [0, 1, 2],
        ...         "measure_a": [5, 4, 6],
        ...         "measure_b": [7, 3, 3],
        ...     }
        ... )

        Emphasize the site_id as row names:

        >>> df.style.tab_stub(rowname_col="site_id")  # doctest: +SKIP

        Fill the background for the highest measure_a value row:

        >>> df.style.tab_style(
        ...     style.fill("yellow"),
        ...     loc.body(rows=pl.col("measure_a") == pl.col("measure_a").max()),
        ... )  # doctest: +SKIP

        Put a spanner (high-level label) over measure columns:

        >>> df.style.tab_spanner(
        ...     "Measures", cs.starts_with("measure")
        ... )  # doctest: +SKIP

        Format measure_b values to two decimal places:

        >>> df.style.fmt_number("measure_b", decimals=2)  # doctest: +SKIP
        """
        if not _GREAT_TABLES_AVAILABLE:
            msg = "great_tables is required for `.style`"
            raise ModuleNotFoundError(msg)

        return great_tables.GT(self)
