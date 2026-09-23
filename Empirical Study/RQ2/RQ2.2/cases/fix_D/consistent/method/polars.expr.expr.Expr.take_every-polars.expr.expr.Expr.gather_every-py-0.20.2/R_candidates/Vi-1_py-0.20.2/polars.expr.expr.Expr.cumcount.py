    @deprecate_renamed_function("cum_count", version="0.19.14")
    def cumcount(self, *, reverse: bool = False) -> Self:
        """
        Get an array with the cumulative count computed at every element.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`cum_count`.

        Parameters
        ----------
        reverse
            Reverse the operation.
        """
        return self.cum_count(reverse=reverse)
