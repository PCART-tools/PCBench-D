    def _iset_item_mgr(
        self, loc: int | slice | np.ndarray, value, inplace: bool = False
    ) -> None:
        # when called from _set_item_mgr loc can be anything returned from get_loc
        self._mgr.iset(loc, value, inplace=inplace)
        self._clear_item_cache()
