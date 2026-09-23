    def _slice_blocks(self, slobj, axis):
        new_blocks = []

        slicer = [slice(None, None) for _ in range(self.ndim)]
        slicer[axis] = slobj
        slicer = tuple(slicer)

        for block in self.blocks:
            newb = make_block(block._slice(slicer),
                              block.items,
                              block.ref_items,
                              klass=block.__class__,
                              fastpath=True,
                              placement=block._ref_locs)
            newb.set_ref_locs(block._ref_locs)
            new_blocks.append(newb)
        return new_blocks
