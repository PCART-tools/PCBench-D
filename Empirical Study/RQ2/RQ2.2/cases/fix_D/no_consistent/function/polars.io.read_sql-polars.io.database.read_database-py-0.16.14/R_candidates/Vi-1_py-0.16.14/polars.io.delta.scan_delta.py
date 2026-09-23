@deprecate_nonkeyword_arguments()
@deprecated_alias(table_uri="source")
def scan_delta(
    source: str,
    version: int | None = None,
    raw_filesystem: pa.fs.FileSystem | None = None,
    storage_options: dict[str, Any] | None = None,
    delta_table_options: dict[str, Any] | None = None,
    pyarrow_options: dict[str, Any] | None = None,
) -> LazyFrame:
    """
    Lazily read from a Delta lake table.

    Parameters
    ----------
    source
        Path or URI to the root of the Delta lake table.

        Note: For Local filesystem, absolute and relative paths are supported. But
        for the supported object storages - GCS, Azure and S3, there is no relative
        path support, and thus full URI must be provided.
    version
        Version of the Delta lake table.

        Note: If ``version`` is not provided, latest version of delta lake
        table is read.
    raw_filesystem
        A `pyarrow.fs.FileSystem` to read files from.

        Note: The root of the filesystem has to be adjusted to point at the root of
        the Delta lake table. The provided ``raw_filesystem`` is wrapped into a
        `pyarrow.fs.SubTreeFileSystem`

        More info is available `here
        <https://delta-io.github.io/delta-rs/python/usage.html?highlight=backend#custom-storage-backends>`__.
    storage_options
        Extra options for the storage backends supported by `deltalake`.
        For cloud storages, this may include configurations for authentication etc.

        More info is available `here
        <https://delta-io.github.io/delta-rs/python/usage.html?highlight=backend#loading-a-delta-table>`__.
    delta_table_options
        Additional keyword arguments while reading a Delta lake Table.
    pyarrow_options
        Keyword arguments while converting a Delta lake Table to pyarrow table.
        Use this parameter when filtering on partitioned columns.

    Returns
    -------
    LazyFrame

    Examples
    --------
    Creates a scan for a Delta table from local filesystem.
    Note: Since version is not provided, latest version of the delta table is read.

    >>> table_path = "/path/to/delta-table/"
    >>> pl.scan_delta(table_path).collect()  # doctest: +SKIP

    Use the `pyarrow_options` parameter to read only certain partitions.

    >>> pl.scan_delta(  # doctest: +SKIP
    ...     table_path,
    ...     pyarrow_options={"partitions": [("year", "=", "2021")]},
    ... )

    Creates a scan for a specific version of the Delta table from local filesystem.
    Note: This will fail if the provided version of the delta table does not exist.

    >>> pl.scan_delta(table_path, version=1).collect()  # doctest: +SKIP

    Creates a scan for a Delta table from AWS S3.
    See a list of supported storage options for S3 `here
    <https://github.com/delta-io/delta-rs/blob/17999d24a58fb4c98c6280b9e57842c346b4603a/rust/src/builder.rs#L423-L491>`__.

    >>> table_path = "s3://bucket/path/to/delta-table/"
    >>> storage_options = {
    ...     "AWS_ACCESS_KEY_ID": "THE_AWS_ACCESS_KEY_ID",
    ...     "AWS_SECRET_ACCESS_KEY": "THE_AWS_SECRET_ACCESS_KEY",
    ... }
    >>> pl.scan_delta(
    ...     table_path, storage_options=storage_options
    ... ).collect()  # doctest: +SKIP

    Creates a scan for a Delta table from Google Cloud storage (GCS).

    Note: This implementation relies on `pyarrow.fs` and thus has to rely on fsspec
    compatible filesystems as mentioned `here
    <https://arrow.apache.org/docs/python/filesystems.html#using-fsspec-compatible-filesystems-with-arrow>`__.
    So please ensure that `pyarrow` ,`fsspec` and `gcsfs` are installed.

    See a list of supported storage options for GCS `here
    <https://github.com/delta-io/delta-rs/blob/17999d24a58fb4c98c6280b9e57842c346b4603a/rust/src/builder.rs#L570-L577>`__.

    >>> import gcsfs  # doctest: +SKIP
    >>> from pyarrow.fs import PyFileSystem, FSSpecHandler  # doctest: +SKIP
    >>> storage_options = {"SERVICE_ACCOUNT": "SERVICE_ACCOUNT_JSON_ABSOLUTE_PATH"}
    >>> fs = gcsfs.GCSFileSystem(
    ...     project="my-project-id",
    ...     token=storage_options["SERVICE_ACCOUNT"],
    ... )  # doctest: +SKIP
    >>> # this pyarrow fs must be created and passed to scan_delta for GCS
    >>> pa_fs = PyFileSystem(FSSpecHandler(fs))  # doctest: +SKIP
    >>> table_path = "gs://bucket/path/to/delta-table/"
    >>> pl.scan_delta(
    ...     table_path, storage_options=storage_options, raw_filesystem=pa_fs
    ... ).collect()  # doctest: +SKIP

    Creates a scan for a Delta table from Azure.

    Note: This implementation relies on `pyarrow.fs` and thus has to rely on fsspec
    compatible filesystems as mentioned `here
    <https://arrow.apache.org/docs/python/filesystems.html#using-fsspec-compatible-filesystems-with-arrow>`__.
    So please ensure that `pyarrow` ,`fsspec` and `adlfs` are installed.

    Following type of table paths are supported,

    * az://<container>/<path>
    * adl://<container>/<path>
    * abfs://<container>/<path>

    See a list of supported storage options for Azure `here
    <https://github.com/delta-io/delta-rs/blob/17999d24a58fb4c98c6280b9e57842c346b4603a/rust/src/builder.rs#L524-L539>`__.

    >>> import adlfs  # doctest: +SKIP
    >>> from pyarrow.fs import PyFileSystem, FSSpecHandler  # doctest: +SKIP
    >>> storage_options = {
    ...     "AZURE_STORAGE_ACCOUNT_NAME": "AZURE_STORAGE_ACCOUNT_NAME",
    ...     "AZURE_STORAGE_ACCOUNT_KEY": "AZURE_STORAGE_ACCOUNT_KEY",
    ... }
    >>> fs = adlfs.AzureBlobFileSystem(
    ...     account_name=storage_options["AZURE_STORAGE_ACCOUNT_NAME"],
    ...     account_key=storage_options["AZURE_STORAGE_ACCOUNT_KEY"],
    ... )  # doctest: +SKIP
    >>> # this pyarrow fs must be created and passed to scan_delta for Azure
    >>> pa_fs = PyFileSystem(FSSpecHandler(fs))  # doctest: +SKIP
    >>> table_path = "az://container/path/to/delta-table/"
    >>> pl.scan_delta(
    ...     table_path, storage_options=storage_options, raw_filesystem=pa_fs
    ... ).collect()  # doctest: +SKIP

    Creates a scan for a Delta table with additional delta specific options.
    In the below example, `without_files` option is used which loads the table without
    file tracking information.

    >>> table_path = "/path/to/delta-table/"
    >>> delta_table_options = {"without_files": True}
    >>> pl.scan_delta(
    ...     table_path, delta_table_options=delta_table_options
    ... ).collect()  # doctest: +SKIP

    """
    if delta_table_options is None:
        delta_table_options = {}

    if pyarrow_options is None:
        pyarrow_options = {}

    import pyarrow.fs as pa_fs

    # Resolve relative paths if not an object storage
    scheme, resolved_uri, normalized_path = _resolve_delta_lake_uri(source)

    # Storage Backend
    if raw_filesystem is None:
        raw_filesystem, normalized_path = pa_fs.FileSystem.from_uri(resolved_uri)

    # SubTreeFileSystem requires normalized path
    subtree_fs_path = resolved_uri if scheme == "" else normalized_path
    filesystem = pa_fs.SubTreeFileSystem(subtree_fs_path, raw_filesystem)

    # deltalake can work with resolved paths
    dl_tbl = _get_delta_lake_table(
        table_path=resolved_uri,
        version=version,
        storage_options=storage_options,
        delta_table_options=delta_table_options,
    )

    # Must provide filesystem as DeltaStorageHandler is not serializable.
    pa_ds = dl_tbl.to_pyarrow_dataset(filesystem=filesystem, **pyarrow_options)
    return scan_pyarrow_dataset(pa_ds)
