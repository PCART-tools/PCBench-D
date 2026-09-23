    def check(self, **kwargs):
        errors = super(DateTimeCheckMixin, self).check(**kwargs)
        errors.extend(self._check_mutually_exclusive_options())
        errors.extend(self._check_fix_default_value())
        return errors
