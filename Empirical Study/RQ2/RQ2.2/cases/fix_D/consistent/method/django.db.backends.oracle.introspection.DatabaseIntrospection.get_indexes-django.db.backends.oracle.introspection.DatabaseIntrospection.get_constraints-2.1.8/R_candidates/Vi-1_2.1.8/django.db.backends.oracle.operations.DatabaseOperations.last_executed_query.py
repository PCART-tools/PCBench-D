    def last_executed_query(self, cursor, sql, params):
        # https://cx-oracle.readthedocs.io/en/latest/cursor.html#Cursor.statement
        # The DB API definition does not define this attribute.
        statement = cursor.statement
        # Unlike Psycopg's `query` and MySQLdb`'s `_executed`, CxOracle's
        # `statement` doesn't contain the query parameters. refs #20010.
        return super().last_executed_query(cursor, statement, params)
