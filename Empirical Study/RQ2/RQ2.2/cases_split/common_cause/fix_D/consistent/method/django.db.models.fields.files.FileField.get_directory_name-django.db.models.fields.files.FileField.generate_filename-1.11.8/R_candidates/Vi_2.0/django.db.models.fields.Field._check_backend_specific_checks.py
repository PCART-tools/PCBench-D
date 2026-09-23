    def _check_backend_specific_checks(self, **kwargs):
        app_label = self.model._meta.app_label
        for db in connections:
            if router.allow_migrate(db, app_label, model_name=self.model._meta.model_name):
                return connections[db].validation.check_field(self, **kwargs)
        return []
