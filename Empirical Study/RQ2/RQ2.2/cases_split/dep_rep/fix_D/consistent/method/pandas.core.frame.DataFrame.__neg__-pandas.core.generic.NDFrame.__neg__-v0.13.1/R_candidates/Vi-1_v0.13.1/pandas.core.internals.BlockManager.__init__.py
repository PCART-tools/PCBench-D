    def __init__(self, blocks, axes, do_integrity_check=True, fastpath=True):
        self.axes = [_ensure_index(ax) for ax in axes]
        self.blocks = blocks

        ndim = self.ndim
        for block in blocks:
            if not block.is_sparse and ndim != block.ndim:
                raise AssertionError(('Number of Block dimensions (%d) must '
                                      'equal number of axes (%d)')
                                     % (block.ndim, ndim))

        if do_integrity_check:
            self._verify_integrity()

        self._has_sparse = False
        self._consolidate_check()

        # we have a duplicate items index, setup the block maps
        if not self.items.is_unique:
            self._set_ref_locs(do_refs=True)
