    def _maybe_update_cacher(self, clear=False, verify_is_copy=True):
        """
        See if we need to update our parent cacher if clear, then clear our
        cache.

        Parameters
        ----------
        clear : boolean, default False
            clear the item cache
        verify_is_copy : boolean, default True
            provide is_copy checks

        """

        cacher = getattr(self, '_cacher', None)
        if cacher is not None:
            ref = cacher[1]()

            # we are trying to reference a dead referant, hence
            # a copy
            if ref is None:
                del self._cacher
            else:
                try:
                    ref._maybe_cache_changed(cacher[0], self)
                except:
                    pass

        if verify_is_copy:
            self._check_setitem_copy(stacklevel=5, t='referant')

        if clear:
            self._clear_item_cache()
