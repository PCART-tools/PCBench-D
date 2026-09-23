    def _to_dict_of_blocks(self, copy: bool = True):
        """
        Return a dict of dtype -> Constructor Types that
        each is a homogeneous dtype.

        Internal ONLY - only works for BlockManager
        """
        mgr = self._mgr
        # convert to BlockManager if needed -> this way support ArrayManager as well
        mgr = mgr_to_mgr(mgr, "block")
        mgr = cast(BlockManager, mgr)
        return {
            k: self._constructor(v).__finalize__(self)
            for k, v, in mgr.to_dict(copy=copy).items()
        }
