    def _init_mgr(self, mgr, axes=None, dtype=None, copy=False):
        """ passed a manager and a axes dict """
        for a, axe in axes.items():
            if axe is not None:
                mgr = mgr.reindex_axis(
                    axe, axis=self._get_block_manager_axis(a), copy=False)

        # do not copy BlockManager unless explicitly done
        if copy and dtype is None:
            mgr = mgr.copy()
        elif dtype is not None:
            # avoid copy if we can
            if len(mgr.blocks) > 1 or mgr.blocks[0].values.dtype != dtype:
                mgr = mgr.astype(dtype=dtype)
        return mgr
