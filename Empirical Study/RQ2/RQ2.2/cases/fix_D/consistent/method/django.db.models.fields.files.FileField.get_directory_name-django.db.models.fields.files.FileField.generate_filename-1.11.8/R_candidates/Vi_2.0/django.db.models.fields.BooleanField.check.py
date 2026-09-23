    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_null(**kwargs))
        return errors
