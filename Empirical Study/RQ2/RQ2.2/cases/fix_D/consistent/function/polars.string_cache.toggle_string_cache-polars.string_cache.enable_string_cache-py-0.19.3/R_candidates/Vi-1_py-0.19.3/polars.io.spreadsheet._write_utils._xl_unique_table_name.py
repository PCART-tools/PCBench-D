def _xl_unique_table_name(wb: Workbook) -> str:
    """Establish a unique (per-workbook) table object name."""
    table_prefix = "Frame"
    polars_tables: set[str] = set()
    for ws in wb.worksheets():
        polars_tables.update(
            tbl["name"] for tbl in ws.tables if tbl["name"].startswith(table_prefix)
        )
    n = len(polars_tables)
    table_name = f"{table_prefix}{n}"
    while table_name in polars_tables:
        n += 1
        table_name = f"{table_prefix}{n}"
    return table_name
