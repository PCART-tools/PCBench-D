    def _replace_coerce(self, to_replace, value, inplace=True, regex=False,
                        convert=False, mask=None):
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
            if not regex:
                self = self.coerce_to_target_dtype(value)
                return self.putmask(mask, value, inplace=inplace)
            else:
                return self._replace_single(to_replace, value, inplace=inplace,
                                            regex=regex,
                                            convert=convert,
                                            mask=mask)
        return self
