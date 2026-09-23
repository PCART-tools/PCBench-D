    def check(self, **kwargs):
        errors = super(CharField, self).check(**kwargs)
        errors.extend(self._check_max_length_attribute(**kwargs))
        return errors
