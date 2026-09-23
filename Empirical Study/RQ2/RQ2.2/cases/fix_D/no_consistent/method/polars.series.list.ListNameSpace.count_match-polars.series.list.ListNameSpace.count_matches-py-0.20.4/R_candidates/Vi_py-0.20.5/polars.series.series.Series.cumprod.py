    @deprecate_renamed_function("cum_prod", version="0.19.14")
    def cumprod(self, *, reverse: bool = False) -> Series:
        """
        Get an array with the cumulative product computed at every element.

        .. deprecated:: 0.19.14
            This method has been renamed to :meth:`cum_prod`.

        Parameters
        ----------
        reverse
            reverse the operation.
        """
        return self.cum_prod(reverse=reverse)
