    @cache_readonly
    def is_all_dates(self):
        return is_datetime_array(self.values)
