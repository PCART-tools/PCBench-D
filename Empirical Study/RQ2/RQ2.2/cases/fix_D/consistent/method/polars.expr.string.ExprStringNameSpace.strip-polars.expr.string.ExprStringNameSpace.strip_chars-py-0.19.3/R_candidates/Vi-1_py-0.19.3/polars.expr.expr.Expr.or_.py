    def or_(self, *others: Any) -> Self:
        """
        Method equivalent of bitwise "or" operator ``expr | other | ...``.

        Parameters
        ----------
        *others
            One or more integer or boolean expressions to evaluate/combine.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     data={
        ...         "x": [5, 6, 7, 4, 8],
        ...         "y": [1.5, 2.5, 1.0, 4.0, -5.75],
        ...         "z": [-9, 2, -1, 4, 8],
        ...     }
        ... )
        >>> df.select(
        ...     (pl.col("x") == pl.col("y"))
        ...     .or_(
        ...         pl.col("x") == pl.col("y"),
        ...         pl.col("y") == pl.col("z"),
        ...         pl.col("y").cast(int) == pl.col("z"),
        ...     )
        ...     .alias("any")
        ... )
        shape: (5, 1)
        ┌───────┐
        │ any   │
        │ ---   │
        │ bool  │
        ╞═══════╡
        │ false │
        │ true  │
        │ false │
        │ true  │
        │ false │
        └───────┘

        """
        return reduce(operator.or_, (self,) + others)
