    def set_sorted(
        self,
        column: str,
        *,
        descending: bool = False,
    ) -> DataFrame:
        """
        Indicate that one or multiple columns are sorted.

        This can speed up future operations.

        Parameters
        ----------
        column
            Column that are sorted
        descending
            Whether the columns are sorted in descending order.

        Warnings
        --------
        This can lead to incorrect results if the data is NOT sorted!!
        Use with care!

        """
        # NOTE: Only accepts 1 column on purpose! User think they are sorted by
        # the combined multicolumn values.
        return (
            self.lazy().set_sorted(column, descending=descending).collect(_eager=True)
        )
