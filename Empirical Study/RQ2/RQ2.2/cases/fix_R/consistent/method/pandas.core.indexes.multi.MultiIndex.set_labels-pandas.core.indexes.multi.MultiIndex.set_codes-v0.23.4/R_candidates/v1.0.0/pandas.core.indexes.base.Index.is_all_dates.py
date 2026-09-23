    @cache_readonly
    def is_all_dates(self) -> bool:
        return is_datetime_array(ensure_object(self.values))
