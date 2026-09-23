    def last_executed_query(self, cursor, sql, params):
        # https://cx-oracle.readthedocs.io/en/latest/cursor.html#Cursor.statement
        # The DB API definition does not define this attribute.
        statement = cursor.statement
        if statement and six.PY2 and not isinstance(statement, unicode):  # NOQA: unicode undefined on PY3
            statement = statement.decode('utf-8')
        # Unlike Psycopg's `query` and MySQLdb`'s `_last_executed`, CxOracle's
        # `statement` doesn't contain the query parameters. refs #20010.
        return super(DatabaseOperations, self).last_executed_query(cursor, statement, params)
