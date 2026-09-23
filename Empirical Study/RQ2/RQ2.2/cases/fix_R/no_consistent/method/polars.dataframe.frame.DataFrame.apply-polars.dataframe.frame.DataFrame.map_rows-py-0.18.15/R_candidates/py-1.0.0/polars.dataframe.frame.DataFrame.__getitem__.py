    def __getitem__(
        self,
        key: (
            SingleIndexSelector
            | SingleColSelector
            | MultiColSelector
            | MultiIndexSelector
            | tuple[SingleIndexSelector, SingleColSelector]
            | tuple[SingleIndexSelector, MultiColSelector]
            | tuple[MultiIndexSelector, SingleColSelector]
            | tuple[MultiIndexSelector, MultiColSelector]
        ),
    ) -> DataFrame | Series | Any:
        """Get part of the DataFrame as a new DataFrame, Series, or scalar."""
        return get_df_item_by_key(self, key)
