    def alter_db_table(self, model, old_db_table, new_db_table, disable_constraints=True):
        if model._meta.related_objects and disable_constraints:
            if self.connection.in_atomic_block:
                raise NotSupportedError((
                    'Renaming the %r table while in a transaction is not '
                    'supported on SQLite because it would break referential '
                    'integrity. Try adding `atomic = False` to the Migration class.'
                ) % old_db_table)
            self.connection.enable_constraint_checking()
            super().alter_db_table(model, old_db_table, new_db_table)
            self.connection.disable_constraint_checking()
        else:
            super().alter_db_table(model, old_db_table, new_db_table)
