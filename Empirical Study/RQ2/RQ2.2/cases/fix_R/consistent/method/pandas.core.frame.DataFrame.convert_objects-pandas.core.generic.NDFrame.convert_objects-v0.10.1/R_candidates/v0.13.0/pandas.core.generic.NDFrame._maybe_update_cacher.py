    def _maybe_update_cacher(self, clear=False):
        """ see if we need to update our parent cacher
            if clear, then clear our cache """
        cacher = getattr(self, '_cacher', None)
        if cacher is not None:
            ref = cacher[1]()

            # we are trying to reference a dead referant, hence
            # a copy
            if ref is None:
                del self._cacher
                self.is_copy = True
                self._check_setitem_copy(stacklevel=5, t='referant')
            else:
                try:
                    ref._maybe_cache_changed(cacher[0], self)
                except:
                    pass
                if ref.is_copy:
                    self.is_copy = True
                    self._check_setitem_copy(stacklevel=5, t='referant')

        if clear:
            self._clear_item_cache()
