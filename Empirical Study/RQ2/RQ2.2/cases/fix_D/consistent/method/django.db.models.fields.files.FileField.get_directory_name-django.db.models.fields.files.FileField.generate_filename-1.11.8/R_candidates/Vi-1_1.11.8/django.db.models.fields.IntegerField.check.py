    def check(self, **kwargs):
        errors = super(IntegerField, self).check(**kwargs)
        errors.extend(self._check_max_length_warning())
        return errors
