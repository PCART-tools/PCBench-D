def handle_projection_columns(
    columns: Sequence[str] | Sequence[int] | str | None,
) -> tuple[list[int] | None, Sequence[str] | None]:
    """Disambiguates between columns specified as integers vs. strings."""
    projection: list[int] | None = None
    new_columns: Sequence[str] | None = None
    if columns is not None:
        if isinstance(columns, str):
            new_columns = [columns]
        elif is_int_sequence(columns):
            projection = list(columns)
        elif not is_str_sequence(columns):
            raise TypeError(
                "'columns' arg should contain a list of all integers or all strings values"
            )
        else:
            new_columns = columns
        if columns and len(set(columns)) != len(columns):
            raise ValueError(
                f"`columns` arg should only have unique values. Got {columns!r}"
            )
        if projection and len(set(projection)) != len(projection):
            raise ValueError(
                f"`columns` arg should only have unique values. Got {projection!r}"
            )
    return projection, new_columns
