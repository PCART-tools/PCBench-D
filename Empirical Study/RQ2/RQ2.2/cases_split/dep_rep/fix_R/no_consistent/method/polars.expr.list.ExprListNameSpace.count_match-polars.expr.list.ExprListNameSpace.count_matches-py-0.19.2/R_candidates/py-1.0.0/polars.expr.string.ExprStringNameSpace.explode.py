    @deprecate_function(
        'Use `.str.split("").explode()` instead.'
        " Note that empty strings will result in null instead of being preserved."
        " To get the exact same behavior, split first and then use when/then/otherwise"
        " to handle the empty list before exploding.",
        version="0.20.31",
    )
    def explode(self) -> Expr:
        """
        Returns a column with a separate row for every string character.

        .. deprecated:: 0.20.31
            Use `.str.split("").explode()` instead.
            Note that empty strings will result in null instead of being preserved.
            To get the exact same behavior, split first and then use when/then/otherwise
            to handle the empty list before exploding.

        Returns
        -------
        Expr
            Expression of data type :class:`String`.

        Examples
        --------
        >>> df = pl.DataFrame({"a": ["foo", "bar"]})
        >>> df.select(pl.col("a").str.explode())  # doctest: +SKIP
        shape: (6, 1)
        ┌─────┐
        │ a   │
        │ --- │
        │ str │
        ╞═════╡
        │ f   │
        │ o   │
        │ o   │
        │ b   │
        │ a   │
        │ r   │
        └─────┘
        """
        split = self.split("")
        return F.when(split.ne_missing([])).then(split).otherwise([""]).explode()
