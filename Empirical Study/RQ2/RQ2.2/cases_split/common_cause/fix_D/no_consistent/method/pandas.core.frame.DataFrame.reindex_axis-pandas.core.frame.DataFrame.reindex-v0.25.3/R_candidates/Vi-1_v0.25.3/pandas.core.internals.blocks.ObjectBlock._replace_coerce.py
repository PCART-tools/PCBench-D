    def _replace_coerce(
        self, to_replace, value, inplace=True, regex=False, convert=False, mask=None
    ):
        """
        Replace value corresponding to the given boolean array with another
        value.

        Parameters
        ----------
        to_replace : object or pattern
            Scalar to replace or regular expression to match.
        value : object
            Replacement object.
        inplace : bool, default False
            Perform inplace modification.
        regex : bool, default False
            If true, perform regular expression substitution.
        convert : bool, default True
            If true, try to coerce any object types to better types.
        mask : array-like of bool, optional
            True indicate corresponding element is ignored.

        Returns
        -------
        A new block if there is anything to replace or the original block.
        """
        if mask.any():
            block = super()._replace_coerce(
                to_replace=to_replace,
                value=value,
                inplace=inplace,
                regex=regex,
                convert=convert,
                mask=mask,
            )
            if convert:
                block = [
                    b.convert(by_item=True, numeric=False, copy=True) for b in block
                ]
            return block
        return self
