    def _iset_item(self, loc: int, value) -> None:
        arraylike = self._sanitize_column(value)
        self._iset_item_mgr(loc, arraylike, inplace=True)

        # check if we are modifying a copy
        # try to set first as we want an invalid
        # value exception to occur first
        if len(self):
            self._check_setitem_copy()
