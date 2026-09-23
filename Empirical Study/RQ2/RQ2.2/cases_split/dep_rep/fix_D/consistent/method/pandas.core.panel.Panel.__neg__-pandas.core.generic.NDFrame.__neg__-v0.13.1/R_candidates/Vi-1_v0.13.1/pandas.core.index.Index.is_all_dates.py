    @cache_readonly
    def is_all_dates(self):
        return self.inferred_type == 'datetime'
