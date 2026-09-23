    def hide_columns(self, subset) -> "Styler":
        """
        Hide columns from rendering.

        Parameters
        ----------
        subset : IndexSlice
            An argument to ``DataFrame.loc`` that identifies which columns
            are hidden.

        Returns
        -------
        self : Styler
        """
        subset = non_reducing_slice(subset)
        hidden_df = self.data.loc[subset]
        self.hidden_columns = self.columns.get_indexer_for(hidden_df.columns)
        return self
