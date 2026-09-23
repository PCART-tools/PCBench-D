    @cache_readonly
    def dtypes(self) -> Series:
        """
        Return the dtypes as a Series for the underlying MultiIndex.
        """
        from pandas import Series

        names = com.fill_missing_names([level.name for level in self.levels])
        return Series([level.dtype for level in self.levels], index=names)
