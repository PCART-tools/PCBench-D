    def unpivot(
        self,
        on: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        *,
        index: ColumnNameOrSelector | Sequence[ColumnNameOrSelector] | None = None,
        variable_name: str | None = None,
        value_name: str | None = None,
        streamable: bool = True,
    ) -> LazyFrame:
        """
        Unpivot a DataFrame from wide to long format.

        Optionally leaves identifiers set.

        This function is useful to massage a DataFrame into a format where one or more
        columns are identifier variables (index) while all other columns, considered
        measured variables (on), are "unpivoted" to the row axis leaving just
        two non-identifier columns, 'variable' and 'value'.

        Parameters
        ----------
        on
            Column(s) or selector(s) to use as values variables; if `on`
            is empty all columns that are not in `index` will be used.
        index
            Column(s) or selector(s) to use as identifier variables.
        variable_name
            Name to give to the `variable` column. Defaults to "variable"
        value_name
            Name to give to the `value` column. Defaults to "value"
        streamable
            Allow this node to run in the streaming engine.
            If this runs in streaming, the output of the unpivot operation
            will not have a stable ordering.

        Notes
        -----
        If you're coming from pandas, this is similar to `pandas.DataFrame.melt`,
        but with `index` replacing `id_vars` and `on` replacing `value_vars`.
        In other frameworks, you might know this operation as `pivot_longer`.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "a": ["x", "y", "z"],
        ...         "b": [1, 3, 5],
        ...         "c": [2, 4, 6],
        ...     }
        ... )
        >>> import polars.selectors as cs
        >>> lf.unpivot(cs.numeric(), index="a").collect()
        shape: (6, 3)
        ┌─────┬──────────┬───────┐
        │ a   ┆ variable ┆ value │
        │ --- ┆ ---      ┆ ---   │
        │ str ┆ str      ┆ i64   │
        ╞═════╪══════════╪═══════╡
        │ x   ┆ b        ┆ 1     │
        │ y   ┆ b        ┆ 3     │
        │ z   ┆ b        ┆ 5     │
        │ x   ┆ c        ┆ 2     │
        │ y   ┆ c        ┆ 4     │
        │ z   ┆ c        ┆ 6     │
        └─────┴──────────┴───────┘
        """
        on = [] if on is None else _expand_selectors(self, on)
        index = [] if index is None else _expand_selectors(self, index)

        return self._from_pyldf(
            self._ldf.unpivot(on, index, value_name, variable_name, streamable)
        )
