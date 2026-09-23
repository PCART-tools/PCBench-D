def _read_sql_connectorx(
    query: str | list[str],
    connection_uri: str,
    partition_on: str | None = None,
    partition_range: tuple[int, int] | None = None,
    partition_num: int | None = None,
    protocol: str | None = None,
    schema_overrides: SchemaDict | None = None,
) -> DataFrame:
    try:
        import connectorx as cx
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "connectorx is not installed"
            "\n\nPlease run `pip install connectorx>=0.3.2`."
        ) from None

    tbl = cx.read_sql(
        conn=connection_uri,
        query=query,
        return_type="arrow2",
        partition_on=partition_on,
        partition_range=partition_range,
        partition_num=partition_num,
        protocol=protocol,
    )
    return from_arrow(tbl, schema_overrides=schema_overrides)  # type: ignore[return-value]
