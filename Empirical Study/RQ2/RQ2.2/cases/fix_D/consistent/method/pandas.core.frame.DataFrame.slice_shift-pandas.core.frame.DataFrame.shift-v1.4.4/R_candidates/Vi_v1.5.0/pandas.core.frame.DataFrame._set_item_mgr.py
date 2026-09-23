    def _set_item_mgr(self, key, value: ArrayLike) -> None:
        try:
            loc = self._info_axis.get_loc(key)
        except KeyError:
            # This item wasn't present, just insert at end
            self._mgr.insert(len(self._info_axis), key, value)
        else:
            self._iset_item_mgr(loc, value)

        # check if we are modifying a copy
        # try to set first as we want an invalid
        # value exception to occur first
        if len(self):
            self._check_setitem_copy()
