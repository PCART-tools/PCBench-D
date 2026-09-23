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
    ) -> LazyFrame:
        """
        Filter the rows in the LazyFrame based on a predicate expression.

        The original order of the remaining rows is preserved.

        Rows where the filter does not evaluate to True are discarded, including nulls.

        Parameters
        ----------
        predicates
            Expression that evaluates to a boolean Series.
        constraints
            Column filters; use `name = value` to filter columns by the supplied value.
            Each constraint will behave the same as `pl.col(name).eq(value)`, and
            will be implicitly joined with the other filter conditions using `&`.

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
                return self.clear()
            elif p is True:
                continue  # no-op; matches all rows
            if _is_generator(p):
                p = tuple(p)
            if is_bool_sequence(p, include_series=True):
                boolean_masks.append(pl.Series(p, dtype=Boolean))
            elif (
                (is_seq := is_sequence(p))
                and any(not isinstance(x, pl.Expr) for x in p)
            ) or (
                not is_seq
                and not isinstance(p, pl.Expr)
                and not (isinstance(p, str) and p in self.collect_schema())
            ):
                err = (
                    f"Series(…, dtype={p.dtype})"
                    if isinstance(p, pl.Series)
                    else repr(p)
                )
                msg = f"invalid predicate for `filter`: {err}"
                raise TypeError(msg)
            else:
                all_predicates.extend(
                    wrap_expr(x) for x in parse_into_list_of_expressions(p)
                )

        # unpack equality constraints from kwargs
        all_predicates.extend(
            F.col(name).eq(value) for name, value in constraints.items()
        )
        if not (all_predicates or boolean_masks):
            msg = "at least one predicate or constraint must be provided"
            raise TypeError(msg)

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
