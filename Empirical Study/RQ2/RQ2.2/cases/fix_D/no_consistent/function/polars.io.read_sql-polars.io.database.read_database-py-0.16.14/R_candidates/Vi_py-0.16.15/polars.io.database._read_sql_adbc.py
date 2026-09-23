def _read_sql_adbc(query: str, connection_uri: str) -> DataFrame:
    with _open_adbc_connection(connection_uri) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        tbl = cursor.fetch_arrow_table()
        cursor.close()
    return from_arrow(tbl)  # type: ignore[return-value]
