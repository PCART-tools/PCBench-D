    @cache_readonly
    def dtypes(self) -> Series:
        """
        Return the dtypes as a Series for the underlying MultiIndex
        """
        from pandas import Series

        return Series(
            {
                f"level_{idx}" if level.name is None else level.name: level.dtype
                for idx, level in enumerate(self.levels)
            }
        )
