    def _iset_item(self, loc: int, value: Series, inplace: bool = True) -> None:
        # We are only called from _replace_columnwise which guarantees that
        # no reindex is necessary
        if using_copy_on_write():
            self._iset_item_mgr(
                loc, value._values, inplace=inplace, refs=value._references
            )
        else:
            self._iset_item_mgr(loc, value._values.copy(), inplace=True)

        # check if we are modifying a copy
        # try to set first as we want an invalid
        # value exception to occur first
        if len(self):
            self._check_setitem_copy()
