def read_database(
    query: list[str] | str,
    connection_uri: str,
    *,
    partition_on: str | None = None,
    partition_range: tuple[int, int] | None = None,
    partition_num: int | None = None,
    protocol: str | None = None,
    engine: DbReadEngine = "connectorx",
) -> DataFrame:
    """
    Read a SQL query into a DataFrame.

    Parameters
    ----------
    query
        Raw SQL query (or queries).
    connection_uri
        A connectorx compatible connection uri, for example

        * "postgresql://username:password@server:port/database"
    partition_on
        The column on which to partition the result.
    partition_range
        The value range of the partition column.
    partition_num
        How many partitions to generate.
    protocol
        Backend-specific transfer protocol directive; see connectorx documentation for
        details.
    engine : {'connectorx', 'adbc'}
        Select the engine used for reading the data.

        * ``'connectorx'``
          Supports a range of databases, such as PostgreSQL, Redshift, MySQL, MariaDB,
          Clickhouse, Oracle, BigQuery, SQL Server, and so on. For an up-to-date list
          please see the connectorx docs:

          * https://github.com/sfu-db/connector-x#supported-sources--destinations
        * ``'adbc'``
          Currently just PostgreSQL and SQLite are supported and these are both in
          development. When flight_sql is further in development and widely adopted
          this will make this significantly better. For an up-to-date list
          please see the adbc docs:

          * https://arrow.apache.org/adbc/0.1.0/driver/cpp/index.html

    Notes
    -----
    Make sure to install connectorx>=0.3.1. Read the documentation
    `here <https://sfu-db.github.io/connector-x/intro.html>`_.

    Examples
    --------
    Read a DataFrame from a SQL query using a single thread:

    >>> uri = "postgresql://username:password@server:port/database"
    >>> query = "SELECT * FROM lineitem"
    >>> pl.read_database(query, uri)  # doctest: +SKIP

    Read a DataFrame in parallel using 10 threads by automatically partitioning the
    provided SQL on the partition column:

    >>> uri = "postgresql://username:password@server:port/database"
    >>> query = "SELECT * FROM lineitem"
    >>> pl.read_database(
    ...     query, uri, partition_on="partition_col", partition_num=10
    ... )  # doctest: +SKIP

    Read a DataFrame in parallel using 2 threads by explicitly providing two SQL
    queries:

    >>> uri = "postgresql://username:password@server:port/database"
    >>> queries = [
    ...     "SELECT * FROM lineitem WHERE partition_col <= 10",
    ...     "SELECT * FROM lineitem WHERE partition_col > 10",
    ... ]
    >>> pl.read_database(queries, uri)  # doctest: +SKIP

    """
    if engine == "connectorx":
        return _read_sql_connectorx(
            query,
            connection_uri,
            partition_on=partition_on,
            partition_range=partition_range,
            partition_num=partition_num,
            protocol=protocol,
        )
    elif engine == "adbc":
        if not isinstance(query, str):
            raise ValueError("Only a single SQL query string is accepted for adbc.")
        return _read_sql_adbc(query, connection_uri)
    else:
        raise ValueError("Engine is not implemented, try either connectorx or adbc.")
