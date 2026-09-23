    def check(self, **kwargs):
        errors = super(FilePathField, self).check(**kwargs)
        errors.extend(self._check_allowing_files_or_folders(**kwargs))
        return errors
