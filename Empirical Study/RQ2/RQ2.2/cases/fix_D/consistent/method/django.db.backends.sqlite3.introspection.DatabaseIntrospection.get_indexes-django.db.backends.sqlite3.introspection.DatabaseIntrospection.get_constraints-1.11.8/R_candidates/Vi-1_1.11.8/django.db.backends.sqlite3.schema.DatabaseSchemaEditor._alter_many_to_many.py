    def _alter_many_to_many(self, model, old_field, new_field, strict):
        """
        Alters M2Ms to repoint their to= endpoints.
        """
        if old_field.remote_field.through._meta.db_table == new_field.remote_field.through._meta.db_table:
            # The field name didn't change, but some options did; we have to propagate this altering.
            self._remake_table(
                old_field.remote_field.through,
                alter_field=(
                    # We need the field that points to the target model, so we can tell alter_field to change it -
                    # this is m2m_reverse_field_name() (as opposed to m2m_field_name, which points to our model)
                    old_field.remote_field.through._meta.get_field(old_field.m2m_reverse_field_name()),
                    new_field.remote_field.through._meta.get_field(new_field.m2m_reverse_field_name()),
                ),
            )
            return

        # Make a new through table
        self.create_model(new_field.remote_field.through)
        # Copy the data across
        self.execute("INSERT INTO %s (%s) SELECT %s FROM %s" % (
            self.quote_name(new_field.remote_field.through._meta.db_table),
            ', '.join([
                "id",
                new_field.m2m_column_name(),
                new_field.m2m_reverse_name(),
            ]),
            ', '.join([
                "id",
                old_field.m2m_column_name(),
                old_field.m2m_reverse_name(),
            ]),
            self.quote_name(old_field.remote_field.through._meta.db_table),
        ))
        # Delete the old through table
        self.delete_model(old_field.remote_field.through)
