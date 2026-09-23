    def get_slice(self, slobj, axis=0, raise_on_error=False):
        new_axes = list(self.axes)

        if raise_on_error:
            _check_slice_bounds(slobj, new_axes[axis])

        new_axes[axis] = new_axes[axis][slobj]

        if axis == 0:
            new_items = new_axes[0]
            if len(self.blocks) == 1:
                blk = self.blocks[0]
                newb = make_block(blk._slice(slobj), new_items, new_items,
                                  klass=blk.__class__, fastpath=True,
                                  placement=blk._ref_locs)
                new_blocks = [newb]
            else:
                return self.reindex_items(
                    new_items, indexer=np.arange(len(self.items))[slobj])
        else:
            new_blocks = self._slice_blocks(slobj, axis)

        bm = self.__class__(new_blocks, new_axes, do_integrity_check=False)
        bm._consolidate_inplace()
        return bm
