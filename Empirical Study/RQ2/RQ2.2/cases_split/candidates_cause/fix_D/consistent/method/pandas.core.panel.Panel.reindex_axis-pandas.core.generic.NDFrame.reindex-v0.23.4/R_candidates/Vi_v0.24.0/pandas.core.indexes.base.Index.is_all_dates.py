    @cache_readonly
    def is_all_dates(self):
        if self._data is None:
            return False
        return is_datetime_array(ensure_object(self.values))
