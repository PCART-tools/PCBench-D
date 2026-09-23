    @deprecate_renamed_function("cum_max", version="0.19.14")
    def cummax(self, *, reverse: bool = False) -> Series:
        """
        Get an array with the cumulative max computed at every element.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`cum_max`.

        Parameters
        ----------
        reverse
            reverse the operation.
        """
        return self.cum_max(reverse=reverse)
