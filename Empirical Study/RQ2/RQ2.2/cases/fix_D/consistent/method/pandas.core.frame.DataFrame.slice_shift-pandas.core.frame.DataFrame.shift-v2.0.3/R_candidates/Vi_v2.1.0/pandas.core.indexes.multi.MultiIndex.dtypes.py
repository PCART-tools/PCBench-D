    @cache_readonly
    def dtypes(self) -> Series:
        """
        Return the dtypes as a Series for the underlying MultiIndex.

        Examples
        --------
        >>> idx = pd.MultiIndex.from_product([(0, 1, 2), ('green', 'purple')],
        ...                                  names=['number', 'color'])
        >>> idx
        MultiIndex([(0,  'green'),
                    (0, 'purple'),
                    (1,  'green'),
                    (1, 'purple'),
                    (2,  'green'),
                    (2, 'purple')],
                   names=['number', 'color'])
        >>> idx.dtypes
        number     int64
        color     object
        dtype: object
        """
        from pandas import Series

        names = com.fill_missing_names([level.name for level in self.levels])
        return Series([level.dtype for level in self.levels], index=Index(names))
