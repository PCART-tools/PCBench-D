    @deprecate_renamed_function("equals", version="0.19.16")
    def frame_equal(self, other: DataFrame, *, null_equal: bool = True) -> bool:
        """
        Check whether the DataFrame is equal to another DataFrame.

        .. deprecated:: 0.19.16
            This method has been renamed to :func:`equals`.

        Parameters
        ----------
        other
            DataFrame to compare with.
        null_equal
            Consider null values as equal.
        """
        return self.equals(other, null_equal=null_equal)
