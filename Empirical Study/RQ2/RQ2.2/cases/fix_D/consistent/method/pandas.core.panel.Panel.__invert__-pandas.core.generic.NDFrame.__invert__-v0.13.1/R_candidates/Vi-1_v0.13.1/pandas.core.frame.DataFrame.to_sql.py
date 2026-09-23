    def to_sql(self, name, con, flavor='sqlite', if_exists='fail', **kwargs):
        """
        Write records stored in a DataFrame to a SQL database.

        Parameters
        ----------
        name : str
            Name of SQL table
        conn : an open SQL database connection object
        flavor: {'sqlite', 'mysql', 'oracle'}, default 'sqlite'
        if_exists: {'fail', 'replace', 'append'}, default 'fail'
            - fail: If table exists, do nothing.
            - replace: If table exists, drop it, recreate it, and insert data.
            - append: If table exists, insert data. Create if does not exist.
        """
        from pandas.io.sql import write_frame
        write_frame(
            self, name, con, flavor=flavor, if_exists=if_exists, **kwargs)
