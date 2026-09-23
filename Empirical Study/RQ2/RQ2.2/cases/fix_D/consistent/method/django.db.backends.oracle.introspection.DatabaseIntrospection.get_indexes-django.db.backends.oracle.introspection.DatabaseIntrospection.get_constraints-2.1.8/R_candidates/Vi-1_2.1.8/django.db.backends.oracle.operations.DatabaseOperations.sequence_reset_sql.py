    def sequence_reset_sql(self, style, model_list):
        from django.db import models
        output = []
        query = self._sequence_reset_sql
        for model in model_list:
            for f in model._meta.local_fields:
                if isinstance(f, models.AutoField):
                    no_autofield_sequence_name = self._get_no_autofield_sequence_name(model._meta.db_table)
                    table = self.quote_name(model._meta.db_table)
                    column = self.quote_name(f.column)
                    output.append(query % {
                        'no_autofield_sequence_name': no_autofield_sequence_name,
                        'table': table,
                        'column': column,
                        'table_name': strip_quotes(table),
                        'column_name': strip_quotes(column),
                    })
                    # Only one AutoField is allowed per model, so don't
                    # continue to loop
                    break
            for f in model._meta.many_to_many:
                if not f.remote_field.through:
                    no_autofield_sequence_name = self._get_no_autofield_sequence_name(f.m2m_db_table())
                    table = self.quote_name(f.m2m_db_table())
                    column = self.quote_name('id')
                    output.append(query % {
                        'no_autofield_sequence_name': no_autofield_sequence_name,
                        'table': table,
                        'column': column,
                        'table_name': strip_quotes(table),
                        'column_name': 'ID',
                    })
        return output
