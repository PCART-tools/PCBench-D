    def replace(self, to_replace, value, inplace=False, filter=None,
                regex=False):
        """ replace the to_replace value with value, possible to create new
        blocks here this is just a call to putmask. regex is not used here.
        It is used in ObjectBlocks.  It is here for API
        compatibility."""
        mask = com.mask_missing(self.values, to_replace)
        if filter is not None:
            for i, item in enumerate(self.items):
                if item not in filter:
                    mask[i] = False

        if not mask.any():
            if inplace:
                return [self]
            return [self.copy()]
        return self.putmask(mask, value, inplace=inplace)
