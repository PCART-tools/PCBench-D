def object() -> SelectorType:
    """
    Select all object columns.

    See Also
    --------
    by_dtype : Select columns by dtype.

    Examples
    --------
    >>> import polars.selectors as cs
    >>> from uuid import uuid4
    >>> with pl.Config(fmt_str_lengths=36):
    ...     df = pl.DataFrame(
    ...         {
    ...             "idx": [0, 1],
    ...             "uuid_obj": [uuid4(), uuid4()],
    ...             "uuid_str": [str(uuid4()), str(uuid4())],
    ...         },
    ...         schema_overrides={"idx": pl.Int32},
    ...     )
    ...     print(df)  # doctest: +IGNORE_RESULT
    ...
    shape: (2, 3)
    ┌─────┬──────────────────────────────────────┬──────────────────────────────────────┐
    │ idx ┆ uuid_obj                             ┆ uuid_str                             │
    │ --- ┆ ---                                  ┆ ---                                  │
    │ i32 ┆ object                               ┆ str                                  │
    ╞═════╪══════════════════════════════════════╪══════════════════════════════════════╡
    │ 0   ┆ 6be063cf-c9c6-43be-878e-e446cfd42981 ┆ acab9fea-c05d-4b91-b639-418004a63f33 │
    │ 1   ┆ 7849d8f9-2cac-48e7-96d3-63cf81c14869 ┆ 28c65415-8b7d-4857-a4ce-300dca14b12b │
    └─────┴──────────────────────────────────────┴──────────────────────────────────────┘

    Select object columns and export as a dict:

    >>> df.select(cs.object()).to_dict(False)  # doctest: +IGNORE_RESULT
    {
        "uuid_obj": [
            UUID("6be063cf-c9c6-43be-878e-e446cfd42981"),
            UUID("7849d8f9-2cac-48e7-96d3-63cf81c14869"),
        ]
    }

    Select all columns *except* for those that are object and export as dict:

    >>> df.select(~cs.object())  # doctest: +IGNORE_RESULT
    {
        "idx": [0, 1],
        "uuid_str": [
            "acab9fea-c05d-4b91-b639-418004a63f33",
            "28c65415-8b7d-4857-a4ce-300dca14b12b",
        ],
    }

    """  # noqa: W505
    return _selector_proxy_(F.col(Object), name="object")
