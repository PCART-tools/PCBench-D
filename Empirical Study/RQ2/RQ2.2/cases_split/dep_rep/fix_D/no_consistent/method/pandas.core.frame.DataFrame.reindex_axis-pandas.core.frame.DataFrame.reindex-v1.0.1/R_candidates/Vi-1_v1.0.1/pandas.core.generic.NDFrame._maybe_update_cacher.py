    def _maybe_update_cacher(
        self, clear: bool_t = False, verify_is_copy: bool_t = True
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

        cacher = getattr(self, "_cacher", None)
        if cacher is not None:
            ref = cacher[1]()

            # we are trying to reference a dead referant, hence
            # a copy
            if ref is None:
                del self._cacher
            else:
                # Note: we need to call ref._maybe_cache_changed even in the
                #  case where it will raise.  (Uh, not clear why)
                try:
                    ref._maybe_cache_changed(cacher[0], self)
                except AssertionError:
                    # ref._data.setitem can raise
                    #  AssertionError because of shape mismatch
                    pass

        if verify_is_copy:
            self._check_setitem_copy(stacklevel=5, t="referant")

        if clear:
            self._clear_item_cache()
