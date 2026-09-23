    @final
    def _format_duplicate_message(self) -> DataFrame:
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

        out = (
            Series(np.arange(len(self)))
            .groupby(self, observed=False)
            .agg(list)[duplicates]
        )
        if self._is_multi:
            # test_format_duplicate_labels_message_multi
            # error: "Type[Index]" has no attribute "from_tuples"  [attr-defined]
            out.index = type(self).from_tuples(out.index)  # type: ignore[attr-defined]

        if self.nlevels == 1:
            out = out.rename_axis("label")
        return out.to_frame(name="positions")
