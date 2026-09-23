    def _create_fk_sql(self, model, field, suffix):
        from_table = model._meta.db_table
        from_column = field.column
        to_table = field.target_field.model._meta.db_table
        to_column = field.target_field.column

        def create_fk_name(*args, **kwargs):
            return self.quote_name(self._create_index_name(*args, **kwargs))

        return Statement(
            self.sql_create_fk,
            table=Table(from_table, self.quote_name),
            name=ForeignKeyName(from_table, [from_column], to_table, [to_column], suffix, create_fk_name),
            column=Columns(from_table, [from_column], self.quote_name),
            to_table=Table(to_table, self.quote_name),
            to_column=Columns(to_table, [to_column], self.quote_name),
            deferrable=self.connection.ops.deferrable_sql(),
        )
