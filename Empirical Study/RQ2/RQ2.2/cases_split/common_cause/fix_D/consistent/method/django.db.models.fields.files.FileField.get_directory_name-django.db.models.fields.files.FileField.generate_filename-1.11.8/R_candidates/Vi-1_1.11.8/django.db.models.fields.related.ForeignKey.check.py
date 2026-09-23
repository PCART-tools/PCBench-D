    def check(self, **kwargs):
        errors = super(ForeignKey, self).check(**kwargs)
        errors.extend(self._check_on_delete())
        errors.extend(self._check_unique())
        return errors
