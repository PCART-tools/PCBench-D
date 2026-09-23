    def add(self, other: Any) -> Self:
        """
        Method equivalent of addition operator ``expr + other``.

        Parameters
        ----------
        other
            numeric or string value; accepts expression input.

        Examples
        --------
        >>> df = pl.DataFrame({"x": [1, 2, 3, 4, 5]})
        >>> df.with_columns(
        ...     pl.col("x").add(2).alias("x+int"),
        ...     pl.col("x").add(pl.col("x").cumprod()).alias("x+expr"),
        ... )
        shape: (5, 3)
        ┌─────┬───────┬────────┐
        │ x   ┆ x+int ┆ x+expr │
        │ --- ┆ ---   ┆ ---    │
        │ i64 ┆ i64   ┆ i64    │
        ╞═════╪═══════╪════════╡
        │ 1   ┆ 3     ┆ 2      │
        │ 2   ┆ 4     ┆ 4      │
        │ 3   ┆ 5     ┆ 9      │
        │ 4   ┆ 6     ┆ 28     │
        │ 5   ┆ 7     ┆ 125    │
        └─────┴───────┴────────┘

        >>> df = pl.DataFrame(
        ...     {"x": ["a", "d", "g"], "y": ["b", "e", "h"], "z": ["c", "f", "i"]}
        ... )
        >>> df.with_columns(pl.col("x").add(pl.col("y")).add(pl.col("z")).alias("xyz"))
        shape: (3, 4)
        ┌─────┬─────┬─────┬─────┐
        │ x   ┆ y   ┆ z   ┆ xyz │
        │ --- ┆ --- ┆ --- ┆ --- │
        │ str ┆ str ┆ str ┆ str │
        ╞═════╪═════╪═════╪═════╡
        │ a   ┆ b   ┆ c   ┆ abc │
        │ d   ┆ e   ┆ f   ┆ def │
        │ g   ┆ h   ┆ i   ┆ ghi │
        └─────┴─────┴─────┴─────┘

        """
        return self.__add__(other)
