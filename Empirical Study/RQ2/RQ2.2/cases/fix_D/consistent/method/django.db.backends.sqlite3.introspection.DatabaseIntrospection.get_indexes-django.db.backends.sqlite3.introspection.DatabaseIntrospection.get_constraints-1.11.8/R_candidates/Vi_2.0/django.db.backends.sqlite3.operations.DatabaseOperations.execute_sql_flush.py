    def execute_sql_flush(self, using, sql_list):
        # To prevent possible violation of foreign key constraints, deactivate
        # constraints outside of the transaction created in super().
        with self.connection.constraint_checks_disabled():
            super().execute_sql_flush(using, sql_list)
