def _from_dataframe_repr(m: re.Match[str]) -> DataFrame:
    """Reconstruct a DataFrame from a regex-matched table repr."""
    from polars.datatypes.convert import dtype_short_repr_to_dtype

    # extract elements from table structure
    lines = m.group().split("\n")[1:-1]
    rows = [
        [re.sub(r"^[\W+]*│", "", elem).strip() for elem in row]
        for row in [re.split("[┆|]", row.rstrip("│ ")) for row in lines]
        if len(row) > 1 or not re.search("├[╌┼]+┤", row[0])
    ]

    # determine beginning/end of the header block
    table_body_start = 2
    for idx, (elem, *_) in enumerate(rows):
        if re.match(r"^\W*╞", elem):
            table_body_start = idx
            break

    # handle headers with wrapped column names and determine headers/dtypes
    header_block = ["".join(h).split("---") for h in zip(*rows[:table_body_start])]
    dtypes: list[str | None]
    if all(len(h) == 1 for h in header_block):
        headers = [h[0] for h in header_block]
        dtypes = [None] * len(headers)
    else:
        headers, dtypes = (list(h) for h in zip_longest(*header_block))

    body = rows[table_body_start + 1 :]
    no_dtypes = all(d is None for d in dtypes)

    # transpose rows into columns, detect/omit truncated columns
    coldata = list(zip(*(row for row in body if not all((e == "…") for e in row))))
    for el in ("…", "..."):
        if el in headers:
            idx = headers.index(el)
            for table_elem in (headers, dtypes):
                table_elem.pop(idx)  # type: ignore[attr-defined]
            if coldata:
                coldata.pop(idx)

    # init cols as utf8 Series, handle "null" -> None, create schema from repr dtype
    data = [pl.Series([(None if v == "null" else v) for v in cd]) for cd in coldata]
    schema = dict(zip(headers, (dtype_short_repr_to_dtype(d) for d in dtypes)))
    for dtype in set(schema.values()):
        if dtype in (List, Struct, Object):
            raise NotImplementedError(
                f"`from_repr` does not support data type {dtype.base_type().__name__!r}"
            )

    # construct DataFrame from string series and cast from repr to native dtype
    df = pl.DataFrame(data=data, orient="col", schema=list(schema))
    if no_dtypes:
        if df.is_empty():
            # if no dtypes *and* empty, default to string
            return df.with_columns(F.all().cast(Utf8))
        else:
            # otherwise, take a trip through our CSV inference logic
            if all(tp == Utf8 for tp in df.schema.values()):
                buf = io.BytesIO()
                df.write_csv(file=buf)
                df = read_csv(buf, new_columns=df.columns, try_parse_dates=True)
            return df
    else:
        return _cast_repr_strings_with_schema(df, schema)
