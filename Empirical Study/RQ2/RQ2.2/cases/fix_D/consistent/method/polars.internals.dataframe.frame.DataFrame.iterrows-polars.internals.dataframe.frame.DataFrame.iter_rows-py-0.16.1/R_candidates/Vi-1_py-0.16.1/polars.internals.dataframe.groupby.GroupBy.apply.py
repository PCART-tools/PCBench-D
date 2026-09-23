    def apply(self, f: Callable[[pli.DataFrame], pli.DataFrame]) -> DF:
        """
        Apply a custom/user-defined function (UDF) over the groups as a sub-DataFrame.

        Implementing logic using a Python function is almost always _significantly_
        slower and more memory intensive than implementing the same logic using
        the native expression API because:

        - The native expression engine runs in Rust; UDFs run in Python.
        - Use of Python UDFs forces the DataFrame to be materialized in memory.
        - Polars-native expressions can be parallelised (UDFs cannot).
        - Polars-native expressions can be logically optimised (UDFs cannot).

        Wherever possible you should strongly prefer the native expression API
        to achieve the best performance.

        Parameters
        ----------
        f
            Custom function.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "id": [0, 1, 2, 3, 4],
        ...         "color": ["red", "green", "green", "red", "red"],
        ...         "shape": ["square", "triangle", "square", "triangle", "square"],
        ...     }
        ... )
        >>> df
        shape: (5, 3)
        ┌─────┬───────┬──────────┐
        │ id  ┆ color ┆ shape    │
        │ --- ┆ ---   ┆ ---      │
        │ i64 ┆ str   ┆ str      │
        ╞═════╪═══════╪══════════╡
        │ 0   ┆ red   ┆ square   │
        │ 1   ┆ green ┆ triangle │
        │ 2   ┆ green ┆ square   │
        │ 3   ┆ red   ┆ triangle │
        │ 4   ┆ red   ┆ square   │
        └─────┴───────┴──────────┘

        For each color group sample two rows:

        >>> df.groupby("color").apply(
        ...     lambda group_df: group_df.sample(2)
        ... )  # doctest: +IGNORE_RESULT
        shape: (4, 3)
        ┌─────┬───────┬──────────┐
        │ id  ┆ color ┆ shape    │
        │ --- ┆ ---   ┆ ---      │
        │ i64 ┆ str   ┆ str      │
        ╞═════╪═══════╪══════════╡
        │ 1   ┆ green ┆ triangle │
        │ 2   ┆ green ┆ square   │
        │ 4   ┆ red   ┆ square   │
        │ 3   ┆ red   ┆ triangle │
        └─────┴───────┴──────────┘

        It is better to implement this with an expression:

        >>> df.filter(
        ...     pl.arange(0, pl.count()).shuffle().over("color") < 2
        ... )  # doctest: +IGNORE_RESULT

        """
        by: Sequence[str]
        if isinstance(self.by, str):
            by = [self.by]
        elif is_str_sequence(self.by):
            by = self.by
        else:
            raise TypeError("Cannot call `apply` when grouping by an expression.")

        return self._dataframe_class._from_pydf(self._df.groupby_apply(by, f))
