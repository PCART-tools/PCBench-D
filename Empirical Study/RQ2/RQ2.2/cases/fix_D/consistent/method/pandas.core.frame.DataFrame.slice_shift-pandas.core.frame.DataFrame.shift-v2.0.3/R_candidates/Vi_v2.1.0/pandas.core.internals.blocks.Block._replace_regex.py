    @final
    def _replace_regex(
        self,
        to_replace,
        value,
        inplace: bool = False,
        mask=None,
        using_cow: bool = False,
    ) -> list[Block]:
        """
        Replace elements by the given value.

        Parameters
        ----------
        to_replace : object or pattern
            Scalar to replace or regular expression to match.
        value : object
            Replacement object.
        inplace : bool, default False
            Perform inplace modification.
        mask : array-like of bool, optional
            True indicate corresponding element is ignored.
        using_cow: bool, default False
            Specifying if copy on write is enabled.

        Returns
        -------
        List[Block]
        """
        if not self._can_hold_element(to_replace):
            # i.e. only if self.is_object is True, but could in principle include a
            #  String ExtensionBlock
            if using_cow:
                return [self.copy(deep=False)]
            return [self] if inplace else [self.copy()]

        rx = re.compile(to_replace)

        block = self._maybe_copy(using_cow, inplace)

        replace_regex(block.values, rx, value, mask)

        return block.convert(copy=False, using_cow=using_cow)
