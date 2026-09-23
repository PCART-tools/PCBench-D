    @classmethod
    def _init_mgr(
        cls,
        mgr: Manager,
        axes,
        dtype: Dtype | None = None,
        copy: bool_t = False,
    ) -> Manager:
        """passed a manager and a axes dict"""
        for a, axe in axes.items():
            if axe is not None:
                axe = ensure_index(axe)
                bm_axis = cls._get_block_manager_axis(a)
                mgr = mgr.reindex_axis(axe, axis=bm_axis)

        # make a copy if explicitly requested
        if copy:
            mgr = mgr.copy()
        if dtype is not None:
            # avoid further copies if we can
            if (
                isinstance(mgr, BlockManager)
                and len(mgr.blocks) == 1
                and is_dtype_equal(mgr.blocks[0].values.dtype, dtype)
            ):
                pass
            else:
                mgr = mgr.astype(dtype=dtype)
        return mgr
