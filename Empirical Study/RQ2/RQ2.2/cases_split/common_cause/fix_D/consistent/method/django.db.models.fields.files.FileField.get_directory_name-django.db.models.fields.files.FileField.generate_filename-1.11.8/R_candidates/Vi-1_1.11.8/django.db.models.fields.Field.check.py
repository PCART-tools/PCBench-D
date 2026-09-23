    def check(self, **kwargs):
        errors = []
        errors.extend(self._check_field_name())
        errors.extend(self._check_choices())
        errors.extend(self._check_db_index())
        errors.extend(self._check_null_allowed_for_primary_keys())
        errors.extend(self._check_backend_specific_checks(**kwargs))
        errors.extend(self._check_deprecation_details())
        return errors
