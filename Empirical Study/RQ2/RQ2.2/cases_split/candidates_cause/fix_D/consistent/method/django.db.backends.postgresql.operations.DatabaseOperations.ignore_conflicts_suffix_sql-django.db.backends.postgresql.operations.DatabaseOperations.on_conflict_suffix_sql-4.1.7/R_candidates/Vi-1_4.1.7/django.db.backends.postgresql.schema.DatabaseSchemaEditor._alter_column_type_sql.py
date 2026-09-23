    def _alter_column_type_sql(self, model, old_field, new_field, new_type):
        self.sql_alter_column_type = "ALTER COLUMN %(column)s TYPE %(type)s"
        # Cast when data type changed.
        using_sql = " USING %(column)s::%(type)s"
        new_internal_type = new_field.get_internal_type()
        old_internal_type = old_field.get_internal_type()
        if new_internal_type == "ArrayField" and new_internal_type == old_internal_type:
            # Compare base data types for array fields.
            if list(self._field_base_data_types(old_field)) != list(
                self._field_base_data_types(new_field)
            ):
                self.sql_alter_column_type += using_sql
        elif self._field_data_type(old_field) != self._field_data_type(new_field):
            self.sql_alter_column_type += using_sql
        # Make ALTER TYPE with IDENTITY make sense.
        table = strip_quotes(model._meta.db_table)
        auto_field_types = {
            "AutoField",
            "BigAutoField",
            "SmallAutoField",
        }
        old_is_auto = old_internal_type in auto_field_types
        new_is_auto = new_internal_type in auto_field_types
        if new_is_auto and not old_is_auto:
            column = strip_quotes(new_field.column)
            return (
                (
                    self.sql_alter_column_type
                    % {
                        "column": self.quote_name(column),
                        "type": new_type,
                    },
                    [],
                ),
                [
                    (
                        self.sql_add_identity
                        % {
                            "table": self.quote_name(table),
                            "column": self.quote_name(column),
                        },
                        [],
                    ),
                ],
            )
        elif old_is_auto and not new_is_auto:
            # Drop IDENTITY if exists (pre-Django 4.1 serial columns don't have
            # it).
            self.execute(
                self.sql_drop_indentity
                % {
                    "table": self.quote_name(table),
                    "column": self.quote_name(strip_quotes(new_field.column)),
                }
            )
            column = strip_quotes(new_field.column)
            fragment, _ = super()._alter_column_type_sql(
                model, old_field, new_field, new_type
            )
            # Drop the sequence if exists (Django 4.1+ identity columns don't
            # have it).
            other_actions = []
            if sequence_name := self._get_sequence_name(table, column):
                other_actions = [
                    (
                        self.sql_delete_sequence
                        % {
                            "sequence": self.quote_name(sequence_name),
                        },
                        [],
                    )
                ]
            return fragment, other_actions
        elif new_is_auto and old_is_auto and old_internal_type != new_internal_type:
            fragment, _ = super()._alter_column_type_sql(
                model, old_field, new_field, new_type
            )
            column = strip_quotes(new_field.column)
            db_types = {
                "AutoField": "integer",
                "BigAutoField": "bigint",
                "SmallAutoField": "smallint",
            }
            # Alter the sequence type if exists (Django 4.1+ identity columns
            # don't have it).
            other_actions = []
            if sequence_name := self._get_sequence_name(table, column):
                other_actions = [
                    (
                        self.sql_alter_sequence_type
                        % {
                            "sequence": self.quote_name(sequence_name),
                            "type": db_types[new_internal_type],
                        },
                        [],
                    ),
                ]
            return fragment, other_actions
        else:
            return super()._alter_column_type_sql(model, old_field, new_field, new_type)
