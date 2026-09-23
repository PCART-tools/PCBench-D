    def _alter_field(self, model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict=False):
        """Perform a "physical" (non-ManyToMany) field update."""
        # Alter by remaking table
        self._remake_table(model, alter_field=(old_field, new_field))
        # Rebuild tables with FKs pointing to this field if the PK type changed.
        if old_field.primary_key and new_field.primary_key and old_type != new_type:
            for rel in new_field.model._meta.related_objects:
                if not rel.many_to_many:
                    self._remake_table(rel.related_model)
