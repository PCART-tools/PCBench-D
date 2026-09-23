    @deprecate_renamed_function("cum_sum", version="0.19.14")
    def cumsum(self, *, reverse: bool = False) -> Self:
        """
        Get an array with the cumulative sum computed at every element.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`cum_sum`.

        Parameters
        ----------
        reverse
            Reverse the operation.
        """
        return self.cum_sum(reverse=reverse)
