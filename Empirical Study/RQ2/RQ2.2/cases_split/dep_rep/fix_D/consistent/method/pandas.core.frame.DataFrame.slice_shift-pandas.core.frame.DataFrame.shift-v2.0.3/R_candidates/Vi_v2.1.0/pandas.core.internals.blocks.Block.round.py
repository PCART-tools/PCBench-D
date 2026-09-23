    @final
    def round(self, decimals: int, using_cow: bool = False) -> Self:
        """
        Rounds the values.
        If the block is not of an integer or float dtype, nothing happens.
        This is consistent with DataFrame.round behavivor.
        (Note: Series.round would raise)

        Parameters
        ----------
        decimals: int,
            Number of decimal places to round to.
            Caller is responsible for validating this
        using_cow: bool,
            Whether Copy on Write is enabled right now
        """
        if not self.is_numeric or self.is_bool:
            return self.copy(deep=not using_cow)
        refs = None
        # TODO: round only defined on BaseMaskedArray
        # Series also does this, so would need to fix both places
        # error: Item "ExtensionArray" of "Union[ndarray[Any, Any], ExtensionArray]"
        # has no attribute "round"
        values = self.values.round(decimals)  # type: ignore[union-attr]
        if values is self.values:
            refs = self.refs
            if not using_cow:
                # Normally would need to do this before, but
                # numpy only returns same array when round operation
                # is no-op
                # https://github.com/numpy/numpy/blob/486878b37fc7439a3b2b87747f50db9b62fea8eb/numpy/core/src/multiarray/calculation.c#L625-L636
                values = values.copy()
        return self.make_block_same_class(values, refs=refs)
