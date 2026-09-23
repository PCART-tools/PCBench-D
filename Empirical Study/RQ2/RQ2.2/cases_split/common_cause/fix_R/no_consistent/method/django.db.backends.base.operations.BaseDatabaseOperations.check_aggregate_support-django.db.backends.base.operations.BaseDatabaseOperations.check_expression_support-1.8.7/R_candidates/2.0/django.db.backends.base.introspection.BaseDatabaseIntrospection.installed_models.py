    def installed_models(self, tables):
        """
        Return a set of all models represented by the provided list of table
        names.
        """
        from django.apps import apps
        from django.db import router
        all_models = []
        for app_config in apps.get_app_configs():
            all_models.extend(router.get_migratable_models(app_config, self.connection.alias))
        tables = list(map(self.table_name_converter, tables))
        return {
            m for m in all_models
            if self.table_name_converter(m._meta.db_table) in tables
        }
