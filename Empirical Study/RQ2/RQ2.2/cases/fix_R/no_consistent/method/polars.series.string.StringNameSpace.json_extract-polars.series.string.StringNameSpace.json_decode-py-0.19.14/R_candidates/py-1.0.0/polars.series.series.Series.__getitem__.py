    def __getitem__(
        self, key: SingleIndexSelector | MultiIndexSelector
    ) -> Any | Series:
        """Get part of the Series as a new Series or scalar."""
        return get_series_item_by_key(self, key)
