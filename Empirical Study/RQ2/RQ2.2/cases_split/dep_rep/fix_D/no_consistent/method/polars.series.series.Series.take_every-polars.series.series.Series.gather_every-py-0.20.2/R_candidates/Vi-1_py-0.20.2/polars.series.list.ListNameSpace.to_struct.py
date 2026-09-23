    def to_struct(
        self,
        n_field_strategy: ToStructStrategy = "first_non_null",
        fields: Callable[[int], str] | Sequence[str] | None = None,
    ) -> Series:
        """
        Convert the series of type `List` to a series of type `Struct`.

        Parameters
        ----------
        n_field_strategy : {'first_non_null', 'max_width'}
            Strategy to determine the number of fields of the struct.

            * "first_non_null": set number of fields equal to the length of the
              first non zero-length sublist.
            * "max_width": set number of fields as max length of all sublists.
        fields
            If the name and number of the desired fields is known in advance
            a list of field names can be given, which will be assigned by index.
            Otherwise, to dynamically assign field names, a custom function can be
            used; if neither are set, fields will be `field_0, field_1 .. field_n`.

        Examples
        --------
        Convert list to struct with default field name assignment:

        >>> s1 = pl.Series("n", [[0, 1, 2], [0, 1]])
        >>> s2 = s1.list.to_struct()
        >>> s2
        shape: (2,)
        Series: 'n' [struct[3]]
        [
            {0,1,2}
            {0,1,null}
        ]
        >>> s2.struct.fields
        ['field_0', 'field_1', 'field_2']

        Convert list to struct with field name assignment by function/index:

        >>> s3 = s1.list.to_struct(fields=lambda idx: f"n{idx:02}")
        >>> s3.struct.fields
        ['n00', 'n01', 'n02']

        Convert list to struct with field name assignment by index from a list of names:

        >>> s1.list.to_struct(fields=["one", "two", "three"]).struct.unnest()
        shape: (2, 3)
        ┌─────┬─────┬───────┐
        │ one ┆ two ┆ three │
        │ --- ┆ --- ┆ ---   │
        │ i64 ┆ i64 ┆ i64   │
        ╞═════╪═════╪═══════╡
        │ 0   ┆ 1   ┆ 2     │
        │ 0   ┆ 1   ┆ null  │
        └─────┴─────┴───────┘

        """
        s = wrap_s(self._s)
        return (
            s.to_frame()
            .select(
                F.col(s.name).list.to_struct(
                    # note: in eager mode, 'upper_bound' is always zero, as (unlike
                    # in lazy mode) there is no need to determine/track the schema.
                    n_field_strategy,
                    fields,
                    upper_bound=0,
                )
            )
            .to_series()
        )
