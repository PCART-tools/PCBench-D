    def _alter_column_collation_sql(
        self, model, new_field, new_type, new_collation, old_field
    ):
        sql = self.sql_alter_column_collate
        # Cast when data type changed.
        if using_sql := self._using_sql(new_field, old_field):
            sql += using_sql
        return (
            sql
            % {
                "column": self.quote_name(new_field.column),
                "type": new_type,
                "collation": " " + self._collate_sql(new_collation)
                if new_collation
                else "",
            },
            [],
        )
