    def merge_sorted(self: DF, other: DataFrame, key: str) -> DF:
        """
        Take two sorted DataFrames and merge them by the sorted key.

        The output of this operation will also be sorted.
        It is the callers responsibility that the frames are sorted
        by that key otherwise the output will not make sense.

        The schemas of both DataFrames must be equal.

        Parameters
        ----------
        other
            Other DataFrame that must be merged
        key
            Key that is sorted.

        """
        return self._from_pydf(
            self.lazy()
            .merge_sorted(other.lazy(), key)
            .collect(no_optimization=True)
            ._df
        )
