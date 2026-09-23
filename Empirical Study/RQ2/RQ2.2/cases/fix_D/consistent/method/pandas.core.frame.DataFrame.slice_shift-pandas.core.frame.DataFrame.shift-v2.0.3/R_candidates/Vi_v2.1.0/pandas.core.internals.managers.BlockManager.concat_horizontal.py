    @classmethod
    def concat_horizontal(cls, mgrs: list[Self], axes: list[Index]) -> Self:
        """
        Concatenate uniformly-indexed BlockManagers horizontally.
        """
        offset = 0
        blocks: list[Block] = []
        for mgr in mgrs:
            for blk in mgr.blocks:
                # We need to do getitem_block here otherwise we would be altering
                #  blk.mgr_locs in place, which would render it invalid. This is only
                #  relevant in the copy=False case.
                nb = blk.slice_block_columns(slice(None))
                nb._mgr_locs = nb._mgr_locs.add(offset)
                blocks.append(nb)

            offset += len(mgr.items)

        new_mgr = cls(tuple(blocks), axes)
        return new_mgr
