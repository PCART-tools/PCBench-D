def _get_delta_lake_table(
    table_path: str,
    version: int | None = None,
    storage_options: dict[str, Any] | None = None,
    delta_table_options: dict[str, Any] | None = None,
) -> deltalake.DeltaTable:
    """
    Initialise a Delta lake table for use in read and scan operations.

    Notes
    -----
    Make sure to install deltalake>=0.8.0. Read the documentation
    `here <https://delta-io.github.io/delta-rs/python/installation.html>`_.

    Returns
    -------
    DeltaTable

    """
    if not _DELTALAKE_AVAILABLE:
        raise ImportError(
            "deltalake is not installed. Please run `pip install deltalake>=0.8.0`."
        )

    if delta_table_options is None:
        delta_table_options = {}

    dl_tbl = deltalake.DeltaTable(
        table_path,
        version=version,
        storage_options=storage_options,
        **delta_table_options,
    )

    return dl_tbl
