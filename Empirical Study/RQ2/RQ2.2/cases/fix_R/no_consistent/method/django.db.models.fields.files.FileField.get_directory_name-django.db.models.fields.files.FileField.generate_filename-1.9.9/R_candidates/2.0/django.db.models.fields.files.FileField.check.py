    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_primary_key())
        errors.extend(self._check_upload_to())
        return errors
