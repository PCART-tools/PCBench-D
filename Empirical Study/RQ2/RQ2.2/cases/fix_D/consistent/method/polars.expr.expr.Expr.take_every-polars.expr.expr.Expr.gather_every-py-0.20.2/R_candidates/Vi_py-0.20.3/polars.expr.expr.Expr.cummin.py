    @deprecate_renamed_function("cum_min", version="0.19.14")
    def cummin(self, *, reverse: bool = False) -> Self:
        """
        Get an array with the cumulative min computed at every element.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`cum_min`.

        Parameters
        ----------
        reverse
            Reverse the operation.
        """
        return self.cum_min(reverse=reverse)
