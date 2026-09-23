    def xor(self, other: Any) -> Self:
        """
        Method equivalent of bitwise exclusive-or operator ``expr ^ other``.

        Parameters
        ----------
        other
            Integer or boolean value; accepts expression input.

        Examples
        --------
        >>> df = pl.DataFrame(
        ...     {"x": [True, False, True, False], "y": [True, True, False, False]}
        ... )
        >>> df.with_columns(pl.col("x").xor(pl.col("y")).alias("x ^ y"))
        shape: (4, 3)
        ┌───────┬───────┬───────┐
        │ x     ┆ y     ┆ x ^ y │
        │ ---   ┆ ---   ┆ ---   │
        │ bool  ┆ bool  ┆ bool  │
        ╞═══════╪═══════╪═══════╡
        │ true  ┆ true  ┆ false │
        │ false ┆ true  ┆ true  │
        │ true  ┆ false ┆ true  │
        │ false ┆ false ┆ false │
        └───────┴───────┴───────┘

        >>> def binary_string(n: int) -> str:
        ...     return bin(n)[2:].zfill(8)
        >>>
        >>> df = pl.DataFrame(
        ...     data={"x": [10, 8, 250, 66], "y": [1, 2, 3, 4]},
        ...     schema={"x": pl.UInt8, "y": pl.UInt8},
        ... )
        >>> df.with_columns(
        ...     pl.col("x").map_elements(binary_string).alias("bin_x"),
        ...     pl.col("y").map_elements(binary_string).alias("bin_y"),
        ...     pl.col("x").xor(pl.col("y")).alias("xor_xy"),
        ...     pl.col("x")
        ...     .xor(pl.col("y"))
        ...     .map_elements(binary_string)
        ...     .alias("bin_xor_xy"),
        ... )
        shape: (4, 6)
        ┌─────┬─────┬──────────┬──────────┬────────┬────────────┐
        │ x   ┆ y   ┆ bin_x    ┆ bin_y    ┆ xor_xy ┆ bin_xor_xy │
        │ --- ┆ --- ┆ ---      ┆ ---      ┆ ---    ┆ ---        │
        │ u8  ┆ u8  ┆ str      ┆ str      ┆ u8     ┆ str        │
        ╞═════╪═════╪══════════╪══════════╪════════╪════════════╡
        │ 10  ┆ 1   ┆ 00001010 ┆ 00000001 ┆ 11     ┆ 00001011   │
        │ 8   ┆ 2   ┆ 00001000 ┆ 00000010 ┆ 10     ┆ 00001010   │
        │ 250 ┆ 3   ┆ 11111010 ┆ 00000011 ┆ 249    ┆ 11111001   │
        │ 66  ┆ 4   ┆ 01000010 ┆ 00000100 ┆ 70     ┆ 01000110   │
        └─────┴─────┴──────────┴──────────┴────────┴────────────┘

        """
        return self.__xor__(other)
