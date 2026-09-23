    def rle(self) -> Series:
        """
        Compress the Series data using run-length encoding.

        Run-length encoding (RLE) encodes data by storing each *run* of identical values
        as a single value and its length.

        Returns
        -------
        Series
            Series of data type `Struct` with fields `len` of data type `UInt32`
            and `value` of the original data type.

        Examples
        --------
        >>> s = pl.Series("s", [1, 1, 2, 1, None, 1, 3, 3])
        >>> s.rle().struct.unnest()
        shape: (6, 2)
        ┌─────┬───────┐
        │ len ┆ value │
        │ --- ┆ ---   │
        │ u32 ┆ i64   │
        ╞═════╪═══════╡
        │ 2   ┆ 1     │
        │ 1   ┆ 2     │
        │ 1   ┆ 1     │
        │ 1   ┆ null  │
        │ 1   ┆ 1     │
        │ 2   ┆ 3     │
        └─────┴───────┘
        """
