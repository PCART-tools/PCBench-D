    def to_sql(self, name, con, flavor='sqlite', schema=None, if_exists='fail',
               index=True, index_label=None, chunksize=None):
        """
        Write records stored in a DataFrame to a SQL database.

        Parameters
        ----------
        name : string
            Name of SQL table
        con : SQLAlchemy engine or DBAPI2 connection (legacy mode)
            Using SQLAlchemy makes it possible to use any DB supported by that
            library.
            If a DBAPI2 object, only sqlite3 is supported.
        flavor : {'sqlite', 'mysql'}, default 'sqlite'
            The flavor of SQL to use. Ignored when using SQLAlchemy engine.
            'mysql' is deprecated and will be removed in future versions, but it
            will be further supported through SQLAlchemy engines.
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

        """
        from pandas.io import sql
        sql.to_sql(
            self, name, con, flavor=flavor, schema=schema, if_exists=if_exists,
            index=index, index_label=index_label, chunksize=chunksize)
