    def to_sql(self, name, con, flavor=None, schema=None, if_exists='fail',
               index=True, index_label=None, chunksize=None, dtype=None):
        """
        Write records stored in a DataFrame to a SQL database.

        Parameters
        ----------
        name : string
            Name of SQL table
        con : SQLAlchemy engine or DBAPI2 connection (legacy mode)
            Using SQLAlchemy makes it possible to use any DB supported by that
            library. If a DBAPI2 object, only sqlite3 is supported.
        flavor : 'sqlite', default None
            .. deprecated:: 0.19.0
               'sqlite' is the only supported option if SQLAlchemy is not
               used.
        schema : string, default None
            Specify the schema (if database flavor supports this). If None, use
            default schema.
        if_exists : {'fail', 'replace', 'append'}, default 'fail'
            - fail: If table exists, do nothing.
            - replace: If table exists, drop it, recreate it, and insert data.
            - append: If table exists, insert data. Create if does not exist.
        index : boolean, default True
            Write DataFrame index as a column.
        index_label : string or sequence, default None
            Column label for index column(s). If None is given (default) and
            `index` is True, then the index names are used.
            A sequence should be given if the DataFrame uses MultiIndex.
        chunksize : int, default None
            If not None, then rows will be written in batches of this size at a
            time.  If None, all rows will be written at once.
        dtype : dict of column name to SQL type, default None
            Optional specifying the datatype for columns. The SQL type should
            be a SQLAlchemy type, or a string for sqlite3 fallback connection.

        """
        from pandas.io import sql
        sql.to_sql(self, name, con, flavor=flavor, schema=schema,
                   if_exists=if_exists, index=index, index_label=index_label,
                   chunksize=chunksize, dtype=dtype)
