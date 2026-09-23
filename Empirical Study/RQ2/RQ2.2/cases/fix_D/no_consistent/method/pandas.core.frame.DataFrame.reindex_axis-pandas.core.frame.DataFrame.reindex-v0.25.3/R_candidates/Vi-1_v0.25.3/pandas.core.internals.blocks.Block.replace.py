    def replace(
        self, to_replace, value, inplace=False, filter=None, regex=False, convert=True
    ):
        """replace the to_replace value with value, possible to create new
        blocks here this is just a call to putmask. regex is not used here.
        It is used in ObjectBlocks.  It is here for API compatibility.
        """

        inplace = validate_bool_kwarg(inplace, "inplace")
        original_to_replace = to_replace

        # try to replace, if we raise an error, convert to ObjectBlock and
        # retry
        values = self._coerce_values(self.values)
        try:
            to_replace = self._try_coerce_args(to_replace)
        except (TypeError, ValueError):
            # GH 22083, TypeError or ValueError occurred within error handling
            # causes infinite loop. Cast and retry only if not objectblock.
            if is_object_dtype(self):
                raise

            # try again with a compatible block
            block = self.astype(object)
            return block.replace(
                to_replace=original_to_replace,
                value=value,
                inplace=inplace,
                filter=filter,
                regex=regex,
                convert=convert,
            )

        mask = missing.mask_missing(values, to_replace)
        if filter is not None:
            filtered_out = ~self.mgr_locs.isin(filter)
            mask[filtered_out.nonzero()[0]] = False

        try:
            blocks = self.putmask(mask, value, inplace=inplace)
        except (TypeError, ValueError):
            # GH 22083, TypeError or ValueError occurred within error handling
            # causes infinite loop. Cast and retry only if not objectblock.
            if is_object_dtype(self):
                raise

            # try again with a compatible block
            block = self.astype(object)
            return block.replace(
                to_replace=original_to_replace,
                value=value,
                inplace=inplace,
                filter=filter,
                regex=regex,
                convert=convert,
            )
        if convert:
            blocks = [
                b.convert(by_item=True, numeric=False, copy=not inplace) for b in blocks
            ]
        return blocks
