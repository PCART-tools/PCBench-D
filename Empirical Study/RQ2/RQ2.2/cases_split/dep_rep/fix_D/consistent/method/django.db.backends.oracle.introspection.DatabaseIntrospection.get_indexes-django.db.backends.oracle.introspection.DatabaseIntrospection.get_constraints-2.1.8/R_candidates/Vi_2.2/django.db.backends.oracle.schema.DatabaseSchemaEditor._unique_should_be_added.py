    def _unique_should_be_added(self, old_field, new_field):
        return (
            super()._unique_should_be_added(old_field, new_field) and
            not self._field_became_primary_key(old_field, new_field)
        )
