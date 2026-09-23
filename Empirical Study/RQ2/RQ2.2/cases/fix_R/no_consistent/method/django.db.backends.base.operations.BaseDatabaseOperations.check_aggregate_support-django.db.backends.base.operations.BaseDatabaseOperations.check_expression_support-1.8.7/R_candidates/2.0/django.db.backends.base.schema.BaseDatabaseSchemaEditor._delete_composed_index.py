    def _delete_composed_index(self, model, fields, constraint_kwargs, sql):
        columns = [model._meta.get_field(field).column for field in fields]
        constraint_names = self._constraint_names(model, columns, **constraint_kwargs)
        if len(constraint_names) != 1:
            raise ValueError("Found wrong number (%s) of constraints for %s(%s)" % (
                len(constraint_names),
                model._meta.db_table,
                ", ".join(columns),
            ))
        self.execute(self._delete_constraint_sql(sql, model, constraint_names[0]))
