    def to_gbq(self, destination_table, schema=None, col_order=None,
               if_exists='fail', **kwargs):
        """Write a DataFrame to a Google BigQuery table.

        If the table exists, the DataFrame will be appended. If not, a new
        table will be created, in which case the schema will have to be
        specified. By default, rows will be written in the order they appear
        in the DataFrame, though the user may specify an alternative order.

        Parameters
        ---------------
        destination_table : string
             name of table to be written, in the form 'dataset.tablename'
        schema : sequence (optional)
             list of column types in order for data to be inserted, e.g.
             ['INTEGER', 'TIMESTAMP', 'BOOLEAN']
        col_order : sequence (optional)
             order which columns are to be inserted, e.g. ['primary_key',
             'birthday', 'username']
        if_exists : {'fail', 'replace', 'append'} (optional)
            - fail: If table exists, do nothing.
            - replace: If table exists, drop it, recreate it, and insert data.
            - append: If table exists, insert data. Create if does not exist.
        kwargs are passed to the Client constructor

        Raises
        ------
        SchemaMissing :
            Raised if the 'if_exists' parameter is set to 'replace', but no
            schema is specified
        TableExists :
            Raised if the specified 'destination_table' exists but the
            'if_exists' parameter is set to 'fail' (the default)
        InvalidSchema :
            Raised if the 'schema' parameter does not match the provided
            DataFrame
        """

        from pandas.io import gbq
        return gbq.to_gbq(self, destination_table, schema=None, col_order=None,
                          if_exists='fail', **kwargs)
