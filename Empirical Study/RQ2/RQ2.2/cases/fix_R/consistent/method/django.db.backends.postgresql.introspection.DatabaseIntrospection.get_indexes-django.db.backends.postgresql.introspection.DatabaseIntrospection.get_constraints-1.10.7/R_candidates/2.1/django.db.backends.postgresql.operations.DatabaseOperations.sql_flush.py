    def sql_flush(self, style, tables, sequences, allow_cascade=False):
        if tables:
            # Perform a single SQL 'TRUNCATE x, y, z...;' statement.  It allows
            # us to truncate tables referenced by a foreign key in any other
            # table.
            tables_sql = ', '.join(
                style.SQL_FIELD(self.quote_name(table)) for table in tables)
            if allow_cascade:
                sql = ['%s %s %s;' % (
                    style.SQL_KEYWORD('TRUNCATE'),
                    tables_sql,
                    style.SQL_KEYWORD('CASCADE'),
                )]
            else:
                sql = ['%s %s;' % (
                    style.SQL_KEYWORD('TRUNCATE'),
                    tables_sql,
                )]
            sql.extend(self.sequence_reset_by_name_sql(style, sequences))
            return sql
        else:
            return []
