    @deprecate_renamed_parameter("if_exists", "if_table_exists", version="0.20.0")
    def write_database(
        self,
        table_name: str,
        connection: str,
        *,
        if_table_exists: DbWriteMode = "fail",
        engine: DbWriteEngine = "sqlalchemy",
    ) -> int:
        """
        Write a polars frame to a database.

        Parameters
        ----------
        table_name
            Schema-qualified name of the table to create or append to in the target
            SQL database. If your table name contains special characters, it should
            be quoted.
        connection
            Connection URI string, for example:

            * "postgresql://user:pass@server:port/database"
            * "sqlite:////path/to/database.db"
        if_table_exists : {'append', 'replace', 'fail'}
            The insert mode:

            * 'replace' will create a new database table, overwriting an existing one.
            * 'append' will append to an existing table.
            * 'fail' will fail if table already exists.
        engine : {'sqlalchemy', 'adbc'}
            Select the engine to use for writing frame data.

        Returns
        -------
        int
            The number of rows affected, if the driver provides this information.
            Otherwise, returns -1.

        """
        from polars.io.database import _open_adbc_connection

        if if_table_exists not in (valid_write_modes := get_args(DbWriteMode)):
            allowed = ", ".join(repr(m) for m in valid_write_modes)
            raise ValueError(
                f"write_database `if_table_exists` must be one of {{{allowed}}}, got {if_table_exists!r}"
            )

        def unpack_table_name(name: str) -> tuple[str | None, str | None, str]:
            """Unpack optionally qualified table name to catalog/schema/table tuple."""
            from csv import reader as delimited_read

            components: list[str | None] = next(delimited_read([name], delimiter="."))  # type: ignore[arg-type]
            if len(components) > 3:
                raise ValueError(f"`table_name` appears to be invalid: '{name}'")
            catalog, schema, tbl = ([None] * (3 - len(components))) + components
            return catalog, schema, tbl  # type: ignore[return-value]

        if engine == "adbc":
            try:
                import adbc_driver_manager

                adbc_version = parse_version(
                    getattr(adbc_driver_manager, "__version__", "0.0")
                )
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    "adbc_driver_manager not found"
                    "\n\nInstall Polars with: pip install adbc_driver_manager"
                ) from exc

            if if_table_exists == "fail":
                # if the table exists, 'create' will raise an error,
                # resulting in behaviour equivalent to 'fail'
                mode = "create"
            elif if_table_exists == "replace":
                if adbc_version < (0, 7):
                    adbc_str_version = ".".join(str(v) for v in adbc_version)
                    raise ModuleUpgradeRequired(
                        f"`if_table_exists = 'replace'` requires ADBC version >= 0.7, found {adbc_str_version}"
                    )
                mode = "replace"
            elif if_table_exists == "append":
                mode = "append"
            else:
                raise ValueError(
                    f"unexpected value for `if_table_exists`: {if_table_exists!r}"
                    f"\n\nChoose one of {{'fail', 'replace', 'append'}}"
                )

            with _open_adbc_connection(connection) as conn, conn.cursor() as cursor:
                catalog, db_schema, unpacked_table_name = unpack_table_name(table_name)
                n_rows: int
                if adbc_version >= (0, 7):
                    if "sqlite" in conn.adbc_get_info()["driver_name"].lower():
                        if if_table_exists == "replace":
                            # note: adbc doesn't (yet) support 'replace' for sqlite
                            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                            mode = "create"
                        catalog, db_schema = db_schema, None

                    n_rows = cursor.adbc_ingest(
                        unpacked_table_name,
                        data=self.to_arrow(),
                        mode=mode,
                        catalog_name=catalog,
                        db_schema_name=db_schema,
                    )
                elif db_schema is not None:
                    adbc_str_version = ".".join(str(v) for v in adbc_version)
                    raise ModuleUpgradeRequired(
                        # https://github.com/apache/arrow-adbc/issues/1000
                        # https://github.com/apache/arrow-adbc/issues/1109
                        f"use of schema-qualified table names requires ADBC version >= 0.8, found {adbc_str_version}"
                    )
                else:
                    n_rows = cursor.adbc_ingest(
                        unpacked_table_name, self.to_arrow(), mode
                    )
                conn.commit()
            return n_rows

        elif engine == "sqlalchemy":
            if not _PANDAS_AVAILABLE:
                raise ModuleNotFoundError(
                    "writing with engine 'sqlalchemy' currently requires pandas.\n\nInstall with: pip install pandas"
                )
            elif parse_version(pd.__version__) < (1, 5):
                raise ModuleUpgradeRequired(
                    f"writing with engine 'sqlalchemy' requires pandas 1.5.x or higher, found {pd.__version__!r}"
                )
            try:
                from sqlalchemy import create_engine
            except ModuleNotFoundError as exc:
                raise ModuleNotFoundError(
                    "sqlalchemy not found\n\nInstall with: pip install polars[sqlalchemy]"
                ) from exc

            # note: the catalog (database) should be a part of the connection string
            engine_sa = create_engine(connection)
            catalog, db_schema, unpacked_table_name = unpack_table_name(table_name)
            if catalog:
                raise ValueError(
                    f"Unexpected three-part table name; provide the database/catalog ({catalog!r}) on the connection URI"
                )

            # ensure conversion to pandas uses the pyarrow extension array option
            # so that we can make use of the sql/db export *without* copying data
            res: int | None = self.to_pandas(
                use_pyarrow_extension_array=True,
            ).to_sql(
                name=unpacked_table_name,
                schema=db_schema,
                con=engine_sa,
                if_exists=if_table_exists,
                index=False,
            )
            return -1 if res is None else res
        else:
            raise ValueError(f"engine {engine!r} is not supported")
