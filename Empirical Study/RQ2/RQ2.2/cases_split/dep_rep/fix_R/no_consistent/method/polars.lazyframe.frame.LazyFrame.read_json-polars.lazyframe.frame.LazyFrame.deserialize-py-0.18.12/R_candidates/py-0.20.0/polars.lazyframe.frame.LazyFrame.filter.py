    def filter(
        self,
        *predicates: (
            IntoExprColumn
            | Iterable[IntoExprColumn]
            | bool
            | list[bool]
            | np.ndarray[Any, Any]
        ),
        **constraints: Any,
    ) -> Self:
        """
        Filter the rows in the LazyFrame based on a predicate expression.

        The original order of the remaining rows is preserved.

        Parameters
        ----------
        predicates
            Expression that evaluates to a boolean Series.
        constraints
            Column filters. Use name=value to filter column name by the supplied value.

        Examples
        --------
        >>> lf = pl.LazyFrame(
        ...     {
        ...         "foo": [1, 2, 3],
        ...         "bar": [6, 7, 8],
        ...         "ham": ["a", "b", "c"],
        ...     }
        ... )

        Filter on one condition:

        >>> lf.filter(pl.col("foo") > 1).collect()
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 2   ┆ 7   ┆ b   │
        │ 3   ┆ 8   ┆ c   │
        └─────┴─────┴─────┘

        Filter on multiple conditions:

        >>> lf.filter((pl.col("foo") < 3) & (pl.col("ham") == "a")).collect()
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6   ┆ a   │
        └─────┴─────┴─────┘

        Provide multiple filters using `*args` syntax:

        >>> lf.filter(
        ...     pl.col("foo") == 1,
        ...     pl.col("ham") == "a",
        ... ).collect()
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6   ┆ a   │
        └─────┴─────┴─────┘

        Provide multiple filters using `**kwargs` syntax:

        >>> lf.filter(foo=1, ham="a").collect()
        shape: (1, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6   ┆ a   │
        └─────┴─────┴─────┘

        Filter on an OR condition:

        >>> lf.filter((pl.col("foo") == 1) | (pl.col("ham") == "c")).collect()
        shape: (2, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ i64 ┆ i64 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6   ┆ a   │
        │ 3   ┆ 8   ┆ c   │
        └─────┴─────┴─────┘

        """
        all_predicates: list[pl.Expr] = []
        boolean_masks = []

        # no-op; immediately matches all rows
        if len(predicates) == 1 and predicates[0] is True and not constraints:
            return self.clone()

        # note: identify masks separately from predicates
        for p in predicates:
            if p is False:  # immediately disallows all rows
                return self.clear()  # type: ignore[return-value]
            elif p is True:
                continue  # no-op; matches all rows
            elif is_bool_sequence(p, include_series=True):
                boolean_masks.append(pl.Series(p, dtype=Boolean))
            elif (
                (is_seq := is_sequence(p))
                and any(not isinstance(x, pl.Expr) for x in p)
            ) or (
                not is_seq
                and not isinstance(p, pl.Expr)
                and not (isinstance(p, str) and p in self.columns)
            ):
                err = (
                    f"Series(…, dtype={p.dtype})"
                    if isinstance(p, pl.Series)
                    else f"{p!r}"
                )
                raise ValueError(f"invalid predicate for `filter`: {err}")
            else:
                all_predicates.extend(
                    wrap_expr(x) for x in parse_as_list_of_expressions(p)
                )

        # identify deprecated usage of 'predicate' parameter
        if "predicate" in constraints:
            is_mask = False
            if isinstance(p := constraints["predicate"], pl.Expr) or (
                is_mask := is_bool_sequence(p)
            ):
                p = constraints.pop("predicate")
                issue_deprecation_warning(
                    "`filter` no longer takes a 'predicate' parameter.\n"
                    "To silence this warning you should omit the keyword and pass "
                    "as a positional argument instead.",
                    version="0.19.9",
                )
                if is_mask:
                    boolean_masks.append(pl.Series(p, dtype=Boolean))
                else:
                    all_predicates.append(p)  # type: ignore[arg-type]

        # unpack equality constraints from kwargs
        all_predicates.extend(
            F.col(name).eq(value) for name, value in constraints.items()
        )
        if not (all_predicates or boolean_masks):
            raise ValueError("No predicates or constraints provided to `filter`.")

        # if multiple predicates, combine as 'horizontal' expression
        combined_predicate = (
            (
                F.all_horizontal(*all_predicates)
                if len(all_predicates) > 1
                else all_predicates[0]
            )._pyexpr
            if all_predicates
            else None
        )

        # apply reduced boolean mask first, if applicable, then predicates
        ldf = (
            self._ldf.filter(F.lit(reduce(and_, boolean_masks))._pyexpr)
            if boolean_masks
            else self._ldf
        )
        return self._from_pyldf(
            ldf if combined_predicate is None else ldf.filter(combined_predicate)
        )
