    def to_init_repr(self, n: int = 1000) -> str:
        """
        Convert DataFrame to instantiatable string representation.

        Parameters
        ----------
        n
            Only use first n rows.

        See Also
        --------
        polars.Series.to_init_repr
        polars.from_repr

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     [
        ...         pl.Series("foo", [1, 2, 3], dtype=pl.UInt8),
        ...         pl.Series("bar", [6.0, 7.0, 8.0], dtype=pl.Float32),
        ...         pl.Series("ham", ["a", "b", "c"], dtype=pl.Utf8),
        ...     ]
        ... )
        >>> print(df.to_init_repr())
        pl.DataFrame(
            [
                pl.Series("foo", [1, 2, 3], dtype=pl.UInt8),
                pl.Series("bar", [6.0, 7.0, 8.0], dtype=pl.Float32),
                pl.Series("ham", ['a', 'b', 'c'], dtype=pl.Utf8),
            ]
        )

        >>> df_from_str_repr = eval(df.to_init_repr())
        >>> df_from_str_repr
        shape: (3, 3)
        ┌─────┬─────┬─────┐
        │ foo ┆ bar ┆ ham │
        │ --- ┆ --- ┆ --- │
        │ u8  ┆ f32 ┆ str │
        ╞═════╪═════╪═════╡
        │ 1   ┆ 6.0 ┆ a   │
        │ 2   ┆ 7.0 ┆ b   │
        │ 3   ┆ 8.0 ┆ c   │
        └─────┴─────┴─────┘

        """
        output = StringIO()
        output.write("pl.DataFrame(\n    [\n")

        for i in range(self.width):
            output.write("        ")
            output.write(self.to_series(i).to_init_repr(n))
            output.write(",\n")

        output.write("    ]\n)\n")

        return output.getvalue()
