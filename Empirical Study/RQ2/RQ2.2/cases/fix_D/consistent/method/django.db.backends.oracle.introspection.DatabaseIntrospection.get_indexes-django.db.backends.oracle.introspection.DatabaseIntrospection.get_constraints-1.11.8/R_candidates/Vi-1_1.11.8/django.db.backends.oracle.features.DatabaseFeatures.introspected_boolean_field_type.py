    def introspected_boolean_field_type(self, field=None, created_separately=False):
        """
        Some versions of Oracle -- we've seen this on 11.2.0.1 and suspect
        it goes back -- have a weird bug where, when an integer column is
        added to an existing table with a default, its precision is later
        reported on introspection as 0, regardless of the real precision.
        For Django introspection, this means that such columns are reported
        as IntegerField even if they are really BigIntegerField or BooleanField.

        The bug is solved in Oracle 11.2.0.2 and up.
        """
        if self.connection.oracle_full_version < '11.2.0.2' and field and field.has_default() and created_separately:
            return 'IntegerField'
        return super(DatabaseFeatures, self).introspected_boolean_field_type(field, created_separately)
