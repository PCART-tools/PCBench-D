    def delete_model(self, model, handle_autom2m=True):
        if handle_autom2m:
            super(DatabaseSchemaEditor, self).delete_model(model)
        else:
            # Delete the table (and only that)
            self.execute(self.sql_delete_table % {
                "table": self.quote_name(model._meta.db_table),
            })
