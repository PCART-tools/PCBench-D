def _merge_blocks(blocks, dtype=None, _can_consolidate=True):

    if len(blocks) == 1:
        return blocks[0]

    if _can_consolidate:

        if dtype is None:
            if len(set([b.dtype for b in blocks])) != 1:
                raise AssertionError("_merge_blocks are invalid!")
            dtype = blocks[0].dtype

        # FIXME: optimization potential in case all mgrs contain slices and
        # combination of those slices is a slice, too.
        new_mgr_locs = np.concatenate([b.mgr_locs.as_array for b in blocks])
        new_values = _vstack([b.values for b in blocks], dtype)

        argsort = np.argsort(new_mgr_locs)
        new_values = new_values[argsort]
        new_mgr_locs = new_mgr_locs[argsort]

        return make_block(new_values, fastpath=True, placement=new_mgr_locs)

    # no merge
    return blocks
