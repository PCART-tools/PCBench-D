    def get_key_columns(self, cursor, table_name):
        """
        Backends can override this to return a list of:
            (column_name, referenced_table_name, referenced_column_name)
        for all key columns in given table.
        """
        raise NotImplementedError('subclasses of BaseDatabaseIntrospection may require a get_key_columns() method')
