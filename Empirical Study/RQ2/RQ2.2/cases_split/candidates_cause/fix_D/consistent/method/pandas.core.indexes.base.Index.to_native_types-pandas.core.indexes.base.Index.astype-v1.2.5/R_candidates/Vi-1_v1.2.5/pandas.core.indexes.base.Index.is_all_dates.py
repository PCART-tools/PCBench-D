    @cache_readonly
    def is_all_dates(self):
        """
        Whether or not the index values only consist of dates.
        """
        warnings.warn(
            "Index.is_all_dates is deprecated, will be removed in a future version.  "
            "check index.inferred_type instead",
            FutureWarning,
            stacklevel=2,
        )
        return self._is_all_dates
