    def sequence_list(self):
        """
        Return a list of information about all DB sequences for all models in
        all apps.
        """
        from django.apps import apps
        from django.db import router

        sequence_list = []
        cursor = self.connection.cursor()

        for app_config in apps.get_app_configs():
            for model in router.get_migratable_models(app_config, self.connection.alias):
                if not model._meta.managed:
                    continue
                if model._meta.swapped:
                    continue
                sequence_list.extend(self.get_sequences(cursor, model._meta.db_table, model._meta.local_fields))
                for f in model._meta.local_many_to_many:
                    # If this is an m2m using an intermediate table,
                    # we don't need to reset the sequence.
                    if f.remote_field.through is None:
                        sequence = self.get_sequences(cursor, f.m2m_db_table())
                        sequence_list.extend(sequence if sequence else [{'table': f.m2m_db_table(), 'column': None}])
        return sequence_list
