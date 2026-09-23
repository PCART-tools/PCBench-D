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
            # i.e. only ObjectBlock, but could in principle include a
            #  String ExtensionBlock
            if using_cow:
                return [self.copy(deep=False)]
            return [self] if inplace else [self.copy()]

        rx = re.compile(to_replace)

        if using_cow:
            if inplace and not self.refs.has_reference():
                refs = self.refs
                new_values = self.values
            else:
                refs = None
                new_values = self.values.copy()
        else:
            refs = None
            new_values = self.values if inplace else self.values.copy()

        replace_regex(new_values, rx, value, mask)

        block = self.make_block(new_values, refs=refs)
        return block.convert(copy=False, using_cow=using_cow)
