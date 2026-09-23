def scan_iceberg(
    source: str | Table,
    *,
    storage_options: dict[str, Any] | None = None,
) -> LazyFrame:
    """
    Lazily read from an Apache Iceberg table.

    Parameters
    ----------
    source
        A PyIceberg table, or a direct path to the metadata.

        Note: For Local filesystem, absolute and relative paths are supported but
        for the supported object storages - GCS, Azure and S3 full URI must be provided.
    storage_options
        Extra options for the storage backends supported by `pyiceberg`.
        For cloud storages, this may include configurations for authentication etc.

        More info is available `here <https://py.iceberg.apache.org/configuration/>`__.

    Returns
    -------
    LazyFrame

    Examples
    --------
    Creates a scan for an Iceberg table from local filesystem, or object store.

    >>> table_path = "file:/path/to/iceberg-table/metadata.json"
    >>> pl.scan_iceberg(table_path).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table from S3.
    See a list of supported storage options for S3 `here
    <https://py.iceberg.apache.org/configuration/#fileio>`__.

    >>> table_path = "s3://bucket/path/to/iceberg-table/metadata.json"
    >>> storage_options = {
    ...     "s3.region": "eu-central-1",
    ...     "s3.access-key-id": "THE_AWS_ACCESS_KEY_ID",
    ...     "s3.secret-access-key": "THE_AWS_SECRET_ACCESS_KEY",
    ... }
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table from Azure.
    Supported options for Azure are available `here
    <https://py.iceberg.apache.org/configuration/#azure-data-lake>`__.

    Following type of table paths are supported:
    * az://<container>/<path>/metadata.json
    * adl://<container>/<path>/metadata.json
    * abfs[s]://<container>/<path>/metadata.json

    >>> table_path = "az://container/path/to/iceberg-table/metadata.json"
    >>> storage_options = {
    ...     "adlfs.account-name": "AZURE_STORAGE_ACCOUNT_NAME",
    ...     "adlfs.account-key": "AZURE_STORAGE_ACCOUNT_KEY",
    ... }
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table from Google Cloud Storage.
    Supported options for GCS are available `here
    <https://py.iceberg.apache.org/configuration/#google-cloud-storage>`__.

    >>> table_path = "s3://bucket/path/to/iceberg-table/metadata.json"
    >>> storage_options = {
    ...     "gcs.project-id": "my-gcp-project",
    ...     "gcs.oauth.token": "ya29.dr.AfM...",
    ... }
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for an Iceberg table with additional options.
    In the below example, `without_files` option is used which loads the table without
    file tracking information.

    >>> table_path = "/path/to/iceberg-table/metadata.json"
    >>> storage_options = {"py-io-impl": "pyiceberg.io.fsspec.FsspecFileIO"}
    >>> pl.scan_iceberg(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    """
    from pyiceberg.io.pyarrow import schema_to_pyarrow
    from pyiceberg.table import StaticTable

    if isinstance(source, str):
        source = StaticTable.from_metadata(
            metadata_location=source, properties=storage_options or {}
        )

    func = partial(_scan_pyarrow_dataset_impl, source)
    arrow_schema = schema_to_pyarrow(source.schema())
    return pl.LazyFrame._scan_python_function(arrow_schema, func, pyarrow=True)
