    def check(self, **kwargs):
        errors = super().check(**kwargs)
        errors.extend(self._check_unique(**kwargs))
        errors.extend(self._check_relationship_model(**kwargs))
        errors.extend(self._check_ignored_options(**kwargs))
        errors.extend(self._check_table_uniqueness(**kwargs))
        return errors
