    def map_groups(self, function: Callable[[DataFrame], DataFrame]) -> DataFrame:
        """
        Apply a custom/user-defined function (UDF) over the groups as a sub-DataFrame.

        .. warning::
            This method is much slower than the native expressions API.
            Only use it if you cannot implement your logic otherwise.

        Implementing logic using a Python function is almost always *significantly*
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
        function
            Custom function that receives a DataFrame and returns a DataFrame.

        Returns
        -------
        DataFrame

        Examples
        --------
        For each color group sample two rows:

        >>> df = pl.DataFrame(
        ...     {
        ...         "id": [0, 1, 2, 3, 4],
        ...         "color": ["red", "green", "green", "red", "red"],
        ...         "shape": ["square", "triangle", "square", "triangle", "square"],
        ...     }
        ... )
        >>> df.group_by("color").map_groups(
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
        ...     pl.int_range(pl.len()).shuffle().over("color") < 2
        ... )  # doctest: +IGNORE_RESULT
        """
        if self.named_by:
            msg = "cannot call `map_groups` when grouping by named expressions"
            raise TypeError(msg)
        if not all(isinstance(c, str) for c in self.by):
            msg = "cannot call `map_groups` when grouping by an expression"
            raise TypeError(msg)

        return self.df.__class__._from_pydf(
            self.df._df.group_by_map_groups(
                list(self.by), function, self.maintain_order
            )
        )
