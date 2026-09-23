    @final
    def _format_duplicate_message(self):
        """
        Construct the DataFrame for a DuplicateLabelError.

        This returns a DataFrame indicating the labels and positions
        of duplicates in an index. This should only be called when it's
        already known that duplicates are present.

        Examples
        --------
        >>> idx = pd.Index(['a', 'b', 'a'])
        >>> idx._format_duplicate_message()
            positions
        label
        a        [0, 2]
        """
        from pandas import Series

        duplicates = self[self.duplicated(keep="first")].unique()
        assert len(duplicates)

        out = Series(np.arange(len(self))).groupby(self).agg(list)[duplicates]
        if self.nlevels == 1:
            out = out.rename_axis("label")
        return out.to_frame(name="positions")
