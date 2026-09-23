    def __init__(self, blocks, axes, do_integrity_check=True, fastpath=True):
        self.axes = [_ensure_index(ax) for ax in axes]
        self.blocks = tuple(blocks)

        for block in blocks:
            if block.is_sparse:
                if len(block.mgr_locs) != 1:
                    raise AssertionError("Sparse block refers to multiple items")
            else:
                if self.ndim != block.ndim:
                    raise AssertionError(('Number of Block dimensions (%d) must '
                                          'equal number of axes (%d)')
                                         % (block.ndim, self.ndim))

        if do_integrity_check:
            self._verify_integrity()

        self._consolidate_check()

        self._rebuild_blknos_and_blklocs()
