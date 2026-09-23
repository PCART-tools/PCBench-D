    def n_unique(
        self, subset: str | pli.Expr | Sequence[str | pli.Expr] | None = None
    ) -> int:
        """
        Return the number of unique rows, or the number of unique row-subsets.

        Parameters
        ----------
        subset
            One or more columns/expressions that define what to count;
            omit to return the count of unique rows.

        Notes
        -----
        This method operates at the ``DataFrame`` level; to operate on subsets at the
        expression level you can make use of struct-packing instead, for example:

        >>> expr_unique_subset = pl.struct(["a", "b"]).n_unique()

        If instead you want to count the number of unique values per-column, you can
        also use expression-level syntax to return a new frame containing that result:

        >>> df = pl.DataFrame([[1, 2, 3], [1, 2, 4]], schema=["a", "b", "c"])
        >>> df_nunique = df.select(pl.all().n_unique())

        In aggregate context there is also an equivalent method for returning the
        unique values per-group:

        >>> df_agg_nunique = df.groupby(by=["a"]).n_unique()

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {
        ...         "a": [1, 1, 2, 3, 4, 5],
        ...         "b": [0.5, 0.5, 1.0, 2.0, 3.0, 3.0],
        ...         "c": [True, True, True, False, True, True],
        ...     }
        ... )
        >>> df.n_unique()
        5
        >>> # simple columns subset
        >>> df.n_unique(subset=["b", "c"])
        4
        >>> # expression subset
        >>> df.n_unique(
        ...     subset=[
        ...         (pl.col("a") // 2),
        ...         (pl.col("c") | (pl.col("b") >= 2)),
        ...     ],
        ... )
        3

        """
        if isinstance(subset, str):
            subset = [pli.col(subset)]
        elif isinstance(subset, pli.Expr):
            subset = [subset]

        if isinstance(subset, Sequence) and len(subset) == 1:
            expr = pli.expr_to_lit_or_expr(subset[0], str_to_lit=False)
        else:
            struct_fields = pli.all() if (subset is None) else subset
            expr = pli.struct(struct_fields)  # type: ignore[call-overload]

        df = self.lazy().select(expr.n_unique()).collect()
        return 0 if df.is_empty() else df.row(0)[0]
