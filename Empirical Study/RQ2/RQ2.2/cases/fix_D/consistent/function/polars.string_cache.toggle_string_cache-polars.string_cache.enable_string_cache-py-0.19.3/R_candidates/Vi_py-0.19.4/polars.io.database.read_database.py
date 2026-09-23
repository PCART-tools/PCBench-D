@deprecate_renamed_parameter("connection_uri", "connection", version="0.18.9")
def read_database(  # noqa: D417
    query: str,
    connection: ConnectionOrCursor,
    *,
    batch_size: int | None = None,
    schema_overrides: SchemaDict | None = None,
    **kwargs: Any,
) -> DataFrame:
    """
    Read the results of a SQL query into a DataFrame, given a connection object.

    Parameters
    ----------
    query
        String SQL query to execute.
    connection
        An instantiated connection (or cursor/client object) that the query can be
        executed against.
    batch_size
        Enable batched data fetching and set the number of rows to fetch each time as
        data is collected. If supported by the backend, it will be passed to the
        underlying query execution method. If the backend does not support changing the
        batch size, it is ignored without error.
    schema_overrides
        A dictionary mapping column names to dtypes, used to override the schema
        inferred from the query cursor or given by the incoming Arrow data (depending
        on driver/backend). This can be useful if the given types can be more precisely
        defined (for example, if you know that a given column can be declared as `u32`
        instead of `i64`).

    Notes
    -----
    * This function supports a wide range of native database drivers (ranging from local
      databases such as SQLite to large cloud databases such as Snowflake), as well as
      generic libraries such as ADBC, SQLAlchemy and various flavours of ODBC. If the
      backend supports returning Arrow data directly then this facility will be used to
      efficiently instantiate the DataFrame; otherwise, the DataFrame is initialised
      from row-wise data.

    * Support for Arrow Flight SQL data is available via the ``adbc-driver-flightsql``
      package; see https://arrow.apache.org/adbc/current/driver/flight_sql.html for
      more details about using this driver (notable databases implementing Flight SQL
      include Dremio and InfluxDB).

    * The ``read_connection_uri`` function is likely to be noticeably faster than
      ``read_database`` if you are using a SQLAlchemy or DBAPI2 connection, as
      ``connectorx`` will optimise translation of the result set into Arrow format
      in Rust, whereas these libraries will return row-wise data to Python *before*
      we can load into Arrow. Note that you can easily determine the connection's
      URI from a SQLAlchemy engine object by calling ``str(conn.engine.url)``.

    * If polars has to create a cursor from your connection in order to execute the
      query then that cursor will be automatically closed when the query completes;
      however, polars will *never* close any other connection or cursor.

    See Also
    --------
    read_database_uri : Create a DataFrame from a SQL query using a URI string.

    Examples
    --------
    Instantiate a DataFrame from a SQL query against a user-supplied connection:

    >>> df = pl.read_database(
    ...     query="SELECT * FROM test_data",
    ...     connection=user_conn,
    ...     schema_overrides={"normalised_score": pl.UInt8},
    ... )  # doctest: +SKIP

    """
    if isinstance(connection, str):
        issue_deprecation_warning(
            message="Use of a string URI with 'read_database' is deprecated; use 'read_database_uri' instead",
            version="0.19.0",
        )
        return read_database_uri(
            query, uri=connection, schema_overrides=schema_overrides, **kwargs
        )
    elif kwargs:
        raise ValueError(
            f"`read_database` **kwargs only exist for deprecating string URIs: found {kwargs!r}"
        )

    with ConnectionExecutor(connection) as cx:
        return cx.execute(query).to_frame(
            batch_size=batch_size,
            schema_overrides=schema_overrides,
        )
