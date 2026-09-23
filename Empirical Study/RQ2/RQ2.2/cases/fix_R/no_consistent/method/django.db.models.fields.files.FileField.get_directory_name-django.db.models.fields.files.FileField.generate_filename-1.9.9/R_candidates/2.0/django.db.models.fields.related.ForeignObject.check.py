    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_to_fields_exist())
        errors.extend(self._check_unique_target())
        return errors
