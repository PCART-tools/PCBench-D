    def _maybe_update_cacher(
        self,
        clear: bool_t = False,
        verify_is_copy: bool_t = True,
        inplace: bool_t = False,
    ) -> None:
        """
        See if we need to update our parent cacher if clear, then clear our
        cache.

        Parameters
        ----------
        clear : bool, default False
            Clear the item cache.
        verify_is_copy : bool, default True
            Provide is_copy checks.
        """

        if verify_is_copy:
            self._check_setitem_copy(t="referent")

        if clear:
            self._clear_item_cache()
