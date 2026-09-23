    def _check_unique_target(self):
        rel_is_string = isinstance(self.remote_field.model, six.string_types)
        if rel_is_string or not self.requires_unique_target:
            return []

        try:
            self.foreign_related_fields
        except exceptions.FieldDoesNotExist:
            return []

        if not self.foreign_related_fields:
            return []

        unique_foreign_fields = {
            frozenset([f.name])
            for f in self.remote_field.model._meta.get_fields()
            if getattr(f, 'unique', False)
        }
        unique_foreign_fields.update({
            frozenset(ut)
            for ut in self.remote_field.model._meta.unique_together
        })
        foreign_fields = {f.name for f in self.foreign_related_fields}
        has_unique_constraint = any(u <= foreign_fields for u in unique_foreign_fields)

        if not has_unique_constraint and len(self.foreign_related_fields) > 1:
            field_combination = ', '.join(
                "'%s'" % rel_field.name for rel_field in self.foreign_related_fields
            )
            model_name = self.remote_field.model.__name__
            return [
                checks.Error(
                    "No subset of the fields %s on model '%s' is unique."
                    % (field_combination, model_name),
                    hint=(
                        "Add unique=True on any of those fields or add at "
                        "least a subset of them to a unique_together constraint."
                    ),
                    obj=self,
                    id='fields.E310',
                )
            ]
        elif not has_unique_constraint:
            field_name = self.foreign_related_fields[0].name
            model_name = self.remote_field.model.__name__
            return [
                checks.Error(
                    "'%s.%s' must set unique=True because it is referenced by "
                    "a foreign key." % (model_name, field_name),
                    obj=self,
                    id='fields.E311',
                )
            ]
        else:
            return []
