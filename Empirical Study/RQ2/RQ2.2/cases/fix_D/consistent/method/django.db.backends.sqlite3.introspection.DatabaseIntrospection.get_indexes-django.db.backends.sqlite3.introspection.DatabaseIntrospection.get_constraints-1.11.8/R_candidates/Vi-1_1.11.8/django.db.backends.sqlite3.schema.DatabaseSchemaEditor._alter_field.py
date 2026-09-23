    def _alter_field(self, model, old_field, new_field, old_type, new_type,
                     old_db_params, new_db_params, strict=False):
        """Actually perform a "physical" (non-ManyToMany) field update."""
        # Alter by remaking table
        self._remake_table(model, alter_field=(old_field, new_field))
