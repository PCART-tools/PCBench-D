    def write_delta(
        self,
        target: str | Path | deltalake.DeltaTable,
        *,
        mode: Literal["error", "append", "overwrite", "ignore", "merge"] = "error",
        overwrite_schema: bool = False,
        storage_options: dict[str, str] | None = None,
        delta_write_options: dict[str, Any] | None = None,
        delta_merge_options: dict[str, Any] | None = None,
    ) -> deltalake.table.TableMerger | None:
        """
        Write DataFrame as delta table.

        Parameters
        ----------
        target
            URI of a table or a DeltaTable object.
        mode : {'error', 'append', 'overwrite', 'ignore', 'merge'}
            How to handle existing data.

            - If 'error', throw an error if the table already exists (default).
            - If 'append', will add new data.
            - If 'overwrite', will replace table with new data.
            - If 'ignore', will not write anything if table already exists.
            - If 'merge', return a `TableMerger` object to merge data from the DataFrame
              with the existing data.
        overwrite_schema
            If True, allows updating the schema of the table.
        storage_options
            Extra options for the storage backends supported by `deltalake`.
            For cloud storages, this may include configurations for authentication etc.

            - See a list of supported storage options for S3 `here <https://docs.rs/object_store/latest/object_store/aws/enum.AmazonS3ConfigKey.html#variants>`__.
            - See a list of supported storage options for GCS `here <https://docs.rs/object_store/latest/object_store/gcp/enum.GoogleConfigKey.html#variants>`__.
            - See a list of supported storage options for Azure `here <https://docs.rs/object_store/latest/object_store/azure/enum.AzureConfigKey.html#variants>`__.
        delta_write_options
            Additional keyword arguments while writing a Delta lake Table.
            See a list of supported write options `here <https://delta-io.github.io/delta-rs/api/delta_writer/#deltalake.write_deltalake>`__.
        delta_merge_options
            Keyword arguments which are required to `MERGE` a Delta lake Table.
            See a list of supported merge options `here <https://delta-io.github.io/delta-rs/api/delta_table/#deltalake.DeltaTable.merge>`__.

        Raises
        ------
        TypeError
            If the DataFrame contains unsupported data types.
        ArrowInvalidError
            If the DataFrame contains data types that could not be cast to their
            primitive type.
        TableNotFoundError
            If the delta table doesn't exist and MERGE action is triggered

        Notes
        -----
        The Polars data types :class:`Null`, :class:`Categorical` and :class:`Time`
        are not supported by the delta protocol specification and will raise a
        TypeError.

        Polars columns are always nullable. To write data to a delta table with
        non-nullable columns, a custom pyarrow schema has to be passed to the
        `delta_write_options`. See the last example below.

        Examples
        --------
        Write a dataframe to the local filesystem as a Delta Lake table.

        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3, 4, 5],
        ...         "bar": [6, 7, 8, 9, 10],
        ...         "ham": ["a", "b", "c", "d", "e"],
        ...     }
        ... )
        >>> table_path = "/path/to/delta-table/"
        >>> df.write_delta(table_path)  # doctest: +SKIP

        Append data to an existing Delta Lake table on the local filesystem.
        Note that this will fail if the schema of the new data does not match the
        schema of the existing table.

        >>> df.write_delta(table_path, mode="append")  # doctest: +SKIP

        Overwrite a Delta Lake table as a new version.
        If the schemas of the new and old data are the same, setting
        `overwrite_schema` is not required.

        >>> existing_table_path = "/path/to/delta-table/"
        >>> df.write_delta(
        ...     existing_table_path, mode="overwrite", overwrite_schema=True
        ... )  # doctest: +SKIP

        Write a DataFrame as a Delta Lake table to a cloud object store like S3.

        >>> table_path = "s3://bucket/prefix/to/delta-table/"
        >>> df.write_delta(
        ...     table_path,
        ...     storage_options={
        ...         "AWS_REGION": "THE_AWS_REGION",
        ...         "AWS_ACCESS_KEY_ID": "THE_AWS_ACCESS_KEY_ID",
        ...         "AWS_SECRET_ACCESS_KEY": "THE_AWS_SECRET_ACCESS_KEY",
        ...     },
        ... )  # doctest: +SKIP

        Write DataFrame as a Delta Lake table with non-nullable columns.

        >>> import pyarrow as pa
        >>> existing_table_path = "/path/to/delta-table/"
        >>> df.write_delta(
        ...     existing_table_path,
        ...     delta_write_options={
        ...         "schema": pa.schema([pa.field("foo", pa.int64(), nullable=False)])
        ...     },
        ... )  # doctest: +SKIP

        Merge the DataFrame with an existing Delta Lake table.
        For all `TableMerger` methods, check the deltalake docs
        `here <https://delta-io.github.io/delta-rs/api/delta_table/delta_table_merger/>`__.

        Schema evolution is not yet supported in by the `deltalake` package, therefore
        `overwrite_schema` will not have any effect on a merge operation.

        >>> df = pl.DataFrame(
        ...     {
        ...         "foo": [1, 2, 3, 4, 5],
        ...         "bar": [6, 7, 8, 9, 10],
        ...         "ham": ["a", "b", "c", "d", "e"],
        ...     }
        ... )
        >>> table_path = "/path/to/delta-table/"
        >>> (
        ...     df.write_delta(
        ...         "table_path",
        ...         mode="merge",
        ...         delta_merge_options={
        ...             "predicate": "s.foo = t.foo",
        ...             "source_alias": "s",
        ...             "target_alias": "t",
        ...         },
        ...     )
        ...     .when_matched_update_all()
        ...     .when_not_matched_insert_all()
        ...     .execute()
        ... )  # doctest: +SKIP
        """
        from polars.io.delta import (
            _check_for_unsupported_types,
            _check_if_delta_available,
            _resolve_delta_lake_uri,
        )

        _check_if_delta_available()

        from deltalake import DeltaTable, write_deltalake

        _check_for_unsupported_types(self.dtypes)

        if isinstance(target, (str, Path)):
            target = _resolve_delta_lake_uri(str(target), strict=False)

        data = self.to_arrow()

        if mode == "merge":
            if delta_merge_options is None:
                raise ValueError(
                    "You need to pass delta_merge_options with at least a given predicate for `MERGE` to work."
                )
            if isinstance(target, str):
                dt = DeltaTable(table_uri=target, storage_options=storage_options)
            else:
                dt = target

            return dt.merge(data, **delta_merge_options)

        else:
            if delta_write_options is None:
                delta_write_options = {}

            schema = delta_write_options.pop("schema", None)
            write_deltalake(
                table_or_uri=target,
                data=data,
                schema=schema,
                mode=mode,
                overwrite_schema=overwrite_schema,
                storage_options=storage_options,
                large_dtypes=True,
                **delta_write_options,
            )
            return None
