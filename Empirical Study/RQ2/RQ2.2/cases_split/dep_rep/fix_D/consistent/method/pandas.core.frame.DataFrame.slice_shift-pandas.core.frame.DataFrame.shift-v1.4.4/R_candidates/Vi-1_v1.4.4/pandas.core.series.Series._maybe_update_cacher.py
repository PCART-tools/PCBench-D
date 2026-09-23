    def _maybe_update_cacher(
        self, clear: bool = False, verify_is_copy: bool = True, inplace: bool = False
    ) -> None:
        """
        See NDFrame._maybe_update_cacher.__doc__
        """
        cacher = getattr(self, "_cacher", None)
        if cacher is not None:
            assert self.ndim == 1
            ref: DataFrame = cacher[1]()

            # we are trying to reference a dead referent, hence
            # a copy
            if ref is None:
                del self._cacher
            elif len(self) == len(ref) and self.name in ref.columns:
                # GH#42530 self.name must be in ref.columns
                # to ensure column still in dataframe
                # otherwise, either self or ref has swapped in new arrays
                ref._maybe_cache_changed(cacher[0], self, inplace=inplace)
            else:
                # GH#33675 we have swapped in a new array, so parent
                #  reference to self is now invalid
                ref._item_cache.pop(cacher[0], None)

        super()._maybe_update_cacher(
            clear=clear, verify_is_copy=verify_is_copy, inplace=inplace
        )
