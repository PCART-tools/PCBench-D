    def check(self, **kwargs):
        errors = super(BooleanField, self).check(**kwargs)
        errors.extend(self._check_null(**kwargs))
        return errors
