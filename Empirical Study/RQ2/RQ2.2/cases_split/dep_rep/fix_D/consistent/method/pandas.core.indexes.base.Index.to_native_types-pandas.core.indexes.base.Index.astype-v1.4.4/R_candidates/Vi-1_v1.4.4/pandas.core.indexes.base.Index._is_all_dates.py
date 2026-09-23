    @cache_readonly
    def _is_all_dates(self) -> bool:
        """
        Whether or not the index values only consist of dates.
        """
        return is_datetime_array(ensure_object(self._values))
