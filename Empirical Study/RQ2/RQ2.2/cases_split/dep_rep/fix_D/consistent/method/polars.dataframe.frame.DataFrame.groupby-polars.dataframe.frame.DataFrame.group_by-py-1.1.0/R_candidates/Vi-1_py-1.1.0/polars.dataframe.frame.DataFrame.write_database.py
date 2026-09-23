    def write_database(
        self,
        table_name: str,
        connection: ConnectionOrCursor | str,
        *,
        if_table_exists: DbWriteMode = "fail",
        engine: DbWriteEngine | None = None,
        engine_options: dict[str, Any] | None = None,
    ) -> int:
        """
        Write the data in a Polars DataFrame to a database.

        .. versionadded:: 0.20.26
            Support for instantiated connection objects in addition to URI strings, and
            a new `engine_options` parameter.

        Parameters
        ----------
        table_name
            Schema-qualified name of the table to create or append to in the target
            SQL database. If your table name contains special characters, it should
            be quoted.
        connection
            An existing SQLAlchemy or ADBC connection against the target database, or
            a URI string that will be used to instantiate such a connection, such as:

            * "postgresql://user:pass@server:port/database"
            * "sqlite:////path/to/database.db"
        if_table_exists : {'append', 'replace', 'fail'}
            The insert mode:

            * 'replace' will create a new database table, overwriting an existing one.
            * 'append' will append to an existing table.
            * 'fail' will fail if table already exists.
        engine : {'sqlalchemy', 'adbc'}
            Select the engine to use for writing frame data; only necessary when
            supplying a URI string (defaults to 'sqlalchemy' if unset)
        engine_options
            Additional options to pass to the engine's associated insert method:

            * "sqlalchemy" - currently inserts using Pandas' `to_sql` method, though
              this will eventually be phased out in favor of a native solution.
            * "adbc" - inserts using the ADBC cursor's `adbc_ingest` method.

        Examples
        --------
        Insert into a temporary table using a PostgreSQL URI and the ADBC engine:

        >>> df.write_database(
        ...     table_name="target_table",
        ...     connection="postgresql://user:pass@server:port/database",
        ...     engine="adbc",
        ...     engine_options={"temporary": True},
        ... )  # doctest: +SKIP

        Insert into a table using a `pyodbc` SQLAlchemy connection to SQL Server
        that was instantiated with "fast_executemany=True" to improve performance:

        >>> pyodbc_uri = (
        ...     "mssql+pyodbc://user:pass@server:1433/test?"
        ...     "driver=ODBC+Driver+18+for+SQL+Server"
        ... )
        >>> engine = create_engine(pyodbc_uri, fast_executemany=True)  # doctest: +SKIP
        >>> df.write_database(
        ...     table_name="target_table",
        ...     connection=engine,
        ... )  # doctest: +SKIP

        Returns
        -------
        int
            The number of rows affected, if the driver provides this information.
            Otherwise, returns -1.
        """
        if if_table_exists not in (valid_write_modes := get_args(DbWriteMode)):
            allowed = ", ".join(repr(m) for m in valid_write_modes)
            msg = f"write_database `if_table_exists` must be one of {{{allowed}}}, got {if_table_exists!r}"
            raise ValueError(msg)

        if engine is None:
            if (
                isinstance(connection, str)
                or (module_root := type(connection).__module__.split(".", 1)[0])
                == "sqlalchemy"
            ):
                engine = "sqlalchemy"
            elif module_root.startswith("adbc"):
                engine = "adbc"

        def unpack_table_name(name: str) -> tuple[str | None, str | None, str]:
            """Unpack optionally qualified table name to catalog/schema/table tuple."""
            from csv import reader as delimited_read

            components: list[str | None] = next(delimited_read([name], delimiter="."))  # type: ignore[arg-type]
            if len(components) > 3:
                msg = f"`table_name` appears to be invalid: '{name}'"
                raise ValueError(msg)
            catalog, schema, tbl = ([None] * (3 - len(components))) + components
            return catalog, schema, tbl  # type: ignore[return-value]

        if engine == "adbc":
            adbc_driver_manager = import_optional("adbc_driver_manager")
            adbc_version = parse_version(
                getattr(adbc_driver_manager, "__version__", "0.0")
            )
            from polars.io.database._utils import _open_adbc_connection

            if if_table_exists == "fail":
                # if the table exists, 'create' will raise an error,
                # resulting in behaviour equivalent to 'fail'
                mode = "create"
            elif if_table_exists == "replace":
                if adbc_version < (0, 7):
                    adbc_str_version = ".".join(str(v) for v in adbc_version)
                    msg = f"`if_table_exists = 'replace'` requires ADBC version >= 0.7, found {adbc_str_version}"
                    raise ModuleUpgradeRequiredError(msg)
                mode = "replace"
            elif if_table_exists == "append":
                mode = "append"
            else:
                msg = (
                    f"unexpected value for `if_table_exists`: {if_table_exists!r}"
                    f"\n\nChoose one of {{'fail', 'replace', 'append'}}"
                )
                raise ValueError(msg)

            conn, can_close_conn = (
                (_open_adbc_connection(connection), True)
                if isinstance(connection, str)
                else (connection, False)
            )
            with (
                conn if can_close_conn else contextlib.nullcontext()
            ), conn.cursor() as cursor:
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
                    msg = f"use of schema-qualified table names requires ADBC version >= 0.8, found {adbc_str_version}"
                    raise ModuleUpgradeRequiredError(
                        # https://github.com/apache/arrow-adbc/issues/1000
                        # https://github.com/apache/arrow-adbc/issues/1109
                        msg
                    )
                else:
                    n_rows = cursor.adbc_ingest(
                        table_name=unpacked_table_name,
                        data=self.to_arrow(),
                        mode=mode,
                        **(engine_options or {}),
                    )
                conn.commit()
            return n_rows

        elif engine == "sqlalchemy":
            if not _PANDAS_AVAILABLE:
                msg = "writing with 'sqlalchemy' engine currently requires pandas.\n\nInstall with: pip install pandas"
                raise ModuleNotFoundError(msg)
            elif (pd_version := parse_version(pd.__version__)) < (1, 5):
                msg = f"writing with 'sqlalchemy' engine requires pandas >= 1.5; found {pd.__version__!r}"
                raise ModuleUpgradeRequiredError(msg)

            import_optional(
                module_name="sqlalchemy",
                min_version=("2.0" if pd_version >= parse_version("2.2") else "1.4"),
                min_err_prefix="pandas >= 2.2 requires",
            )
            # note: the catalog (database) should be a part of the connection string
            from sqlalchemy.engine import create_engine
            from sqlalchemy.orm import Session

            if isinstance(connection, str):
                engine_sa = create_engine(connection)
            elif isinstance(connection, Session):
                engine_sa = connection.connection().engine
            else:
                engine_sa = connection.engine  # type: ignore[union-attr]

            catalog, db_schema, unpacked_table_name = unpack_table_name(table_name)
            if catalog:
                msg = f"Unexpected three-part table name; provide the database/catalog ({catalog!r}) on the connection URI"
                raise ValueError(msg)

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
                **(engine_options or {}),
            )
            return -1 if res is None else res

        elif isinstance(engine, str):
            msg = f"engine {engine!r} is not supported"
            raise ValueError(msg)
        else:
            msg = f"unrecognised connection type {connection!r}"
            raise TypeError(msg)
