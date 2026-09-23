    def introspected_boolean_field_type(self, field=None):
        """
        What is the type returned when the backend introspects a BooleanField?
        The `field` argument may be used to give further details of the field
        to be introspected.

        The return value from this function is compared by tests against actual
        introspection results; it should provide expectations, not run an
        introspection itself.
        """
        if self.can_introspect_null and field and field.null:
            return 'NullBooleanField'
        return 'BooleanField'
