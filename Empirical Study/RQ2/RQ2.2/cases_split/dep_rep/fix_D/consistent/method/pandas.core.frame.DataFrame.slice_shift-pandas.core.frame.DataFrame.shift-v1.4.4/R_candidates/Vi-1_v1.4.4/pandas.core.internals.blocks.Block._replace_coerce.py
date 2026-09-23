    @final
    def _replace_coerce(
        self,
        to_replace,
        value,
        mask: np.ndarray,
        inplace: bool = True,
        regex: bool = False,
    ) -> list[Block]:
        """
        Replace value corresponding to the given boolean array with another
        value.

        Parameters
        ----------
        to_replace : object or pattern
            Scalar to replace or regular expression to match.
        value : object
            Replacement object.
        mask : np.ndarray[bool]
            True indicate corresponding element is ignored.
        inplace : bool, default True
            Perform inplace modification.
        regex : bool, default False
            If true, perform regular expression substitution.

        Returns
        -------
        List[Block]
        """
        if should_use_regex(regex, to_replace):
            return self._replace_regex(
                to_replace,
                value,
                inplace=inplace,
                convert=False,
                mask=mask,
            )
        else:
            if value is None:
                # gh-45601, gh-45836, gh-46634
                if mask.any():
                    nb = self.astype(np.dtype(object), copy=False)
                    if nb is self and not inplace:
                        nb = nb.copy()
                    putmask_inplace(nb.values, mask, value)
                    return [nb]
                return [self] if inplace else [self.copy()]
            return self.replace(
                to_replace=to_replace, value=value, inplace=inplace, mask=mask
            )
