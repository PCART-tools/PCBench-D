    @final
    def replace(
        self,
        to_replace,
        value,
        inplace: bool = False,
        # mask may be pre-computed if we're called from replace_list
        mask: npt.NDArray[np.bool_] | None = None,
    ) -> list[Block]:
        """
        replace the to_replace value with value, possible to create new
        blocks here this is just a call to putmask.
        """

        # Note: the checks we do in NDFrame.replace ensure we never get
        #  here with listlike to_replace or value, as those cases
        #  go through replace_list

        values = self.values

        if isinstance(values, Categorical):
            # TODO: avoid special-casing
            blk = self if inplace else self.copy()
            blk.values._replace(to_replace=to_replace, value=value, inplace=True)
            return [blk]

        if not self._can_hold_element(to_replace):
            # We cannot hold `to_replace`, so we know immediately that
            #  replacing it is a no-op.
            # Note: If to_replace were a list, NDFrame.replace would call
            #  replace_list instead of replace.
            return [self] if inplace else [self.copy()]

        if mask is None:
            mask = missing.mask_missing(values, to_replace)
        if not mask.any():
            # Note: we get here with test_replace_extension_other incorrectly
            #  bc _can_hold_element is incorrect.
            return [self] if inplace else [self.copy()]

        elif self._can_hold_element(value):
            blk = self if inplace else self.copy()
            putmask_inplace(blk.values, mask, value)
            if not (self.is_object and value is None):
                # if the user *explicitly* gave None, we keep None, otherwise
                #  may downcast to NaN
                blocks = blk.convert(numeric=False, copy=False)
            else:
                blocks = [blk]
            return blocks

        elif self.ndim == 1 or self.shape[0] == 1:
            blk = self.coerce_to_target_dtype(value)
            return blk.replace(
                to_replace=to_replace,
                value=value,
                inplace=True,
                mask=mask,
            )

        else:
            # split so that we only upcast where necessary
            blocks = []
            for i, nb in enumerate(self._split()):
                blocks.extend(
                    type(self).replace(
                        nb,
                        to_replace=to_replace,
                        value=value,
                        inplace=True,
                        mask=mask[i : i + 1],
                    )
                )
            return blocks
