    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_allowing_files_or_folders(**kwargs))
        return errors
