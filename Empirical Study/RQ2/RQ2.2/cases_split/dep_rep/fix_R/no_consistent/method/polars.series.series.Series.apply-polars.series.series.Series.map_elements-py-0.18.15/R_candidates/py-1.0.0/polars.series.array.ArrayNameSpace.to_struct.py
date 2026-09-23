    def to_struct(
        self,
        fields: Callable[[int], str] | Sequence[str] | None = None,
    ) -> Series:
        """
        Convert the series of type `Array` to a series of type `Struct`.

        Parameters
        ----------
        fields
            If the name and number of the desired fields is known in advance
            a list of field names can be given, which will be assigned by index.
            Otherwise, to dynamically assign field names, a custom function can be
            used; if neither are set, fields will be `field_0, field_1 .. field_n`.

        Examples
        --------
        Convert array to struct with default field name assignment:

        >>> s1 = pl.Series("n", [[0, 1, 2], [3, 4, 5]], dtype=pl.Array(pl.Int8, 3))
        >>> s2 = s1.arr.to_struct()
        >>> s2
        shape: (2,)
        Series: 'n' [struct[3]]
        [
            {0,1,2}
            {3,4,5}
        ]
        >>> s2.struct.fields
        ['field_0', 'field_1', 'field_2']

        Convert array to struct with field name assignment by function/index:

        >>> s3 = s1.arr.to_struct(fields=lambda idx: f"n{idx:02}")
        >>> s3.struct.fields
        ['n00', 'n01', 'n02']

        Convert array to struct with field name assignment by
        index from a list of names:

        >>> s1.arr.to_struct(fields=["one", "two", "three"]).struct.unnest()
        shape: (2, 3)
        ┌─────┬─────┬───────┐
        │ one ┆ two ┆ three │
        │ --- ┆ --- ┆ ---   │
        │ i8  ┆ i8  ┆ i8    │
        ╞═════╪═════╪═══════╡
        │ 0   ┆ 1   ┆ 2     │
        │ 3   ┆ 4   ┆ 5     │
        └─────┴─────┴───────┘
        """
        s = wrap_s(self._s)
        return s.to_frame().select(F.col(s.name).arr.to_struct(fields)).to_series()
