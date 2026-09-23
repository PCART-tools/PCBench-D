    def check(self, **kwargs):
        errors = super(GenericIPAddressField, self).check(**kwargs)
        errors.extend(self._check_blank_and_null_values(**kwargs))
        return errors
