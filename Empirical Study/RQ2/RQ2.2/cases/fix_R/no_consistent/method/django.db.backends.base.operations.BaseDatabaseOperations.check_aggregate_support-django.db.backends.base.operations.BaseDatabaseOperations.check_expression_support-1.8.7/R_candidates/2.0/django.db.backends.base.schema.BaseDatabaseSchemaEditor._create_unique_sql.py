    def _create_unique_sql(self, model, columns):
        table = model._meta.db_table
        return Statement(
            self.sql_create_unique,
            table=Table(table, self.quote_name),
            name=IndexName(table, columns, '_uniq', self._create_index_name),
            columns=Columns(table, columns, self.quote_name),
        )
