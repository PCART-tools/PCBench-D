    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_max_length_attribute(**kwargs))
        return errors
