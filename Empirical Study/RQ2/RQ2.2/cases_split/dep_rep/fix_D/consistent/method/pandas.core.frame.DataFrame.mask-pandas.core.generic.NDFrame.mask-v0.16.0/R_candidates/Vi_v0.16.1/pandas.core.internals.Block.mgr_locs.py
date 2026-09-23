    @mgr_locs.setter
    def mgr_locs(self, new_mgr_locs):
        if not isinstance(new_mgr_locs, BlockPlacement):
            new_mgr_locs = BlockPlacement(new_mgr_locs)

        self._mgr_locs = new_mgr_locs
