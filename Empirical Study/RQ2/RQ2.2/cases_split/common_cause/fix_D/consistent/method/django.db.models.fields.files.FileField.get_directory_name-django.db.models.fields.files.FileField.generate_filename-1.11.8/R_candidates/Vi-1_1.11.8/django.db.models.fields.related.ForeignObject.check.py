    def check(self, **kwargs):
        errors = super(ForeignObject, self).check(**kwargs)
        errors.extend(self._check_to_fields_exist())
        errors.extend(self._check_unique_target())
        return errors
