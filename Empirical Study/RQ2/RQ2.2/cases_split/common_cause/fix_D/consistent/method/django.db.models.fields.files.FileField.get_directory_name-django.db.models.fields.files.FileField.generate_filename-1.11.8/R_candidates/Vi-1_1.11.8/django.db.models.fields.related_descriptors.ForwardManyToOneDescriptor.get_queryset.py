    def get_queryset(self, **hints):
        related_model = self.field.remote_field.model

        if getattr(related_model._default_manager, 'use_for_related_fields', False):
            if not getattr(related_model._default_manager, 'silence_use_for_related_fields_deprecation', False):
                warnings.warn(
                    "use_for_related_fields is deprecated, instead "
                    "set Meta.base_manager_name on '{}'.".format(related_model._meta.label),
                    RemovedInDjango20Warning, 2
                )
            manager = related_model._default_manager
        else:
            manager = related_model._base_manager

        return manager.db_manager(hints=hints).all()
