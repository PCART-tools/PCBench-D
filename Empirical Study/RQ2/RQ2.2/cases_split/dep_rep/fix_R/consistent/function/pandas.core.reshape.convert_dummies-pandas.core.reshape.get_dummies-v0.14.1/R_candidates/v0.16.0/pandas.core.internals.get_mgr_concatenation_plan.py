def get_mgr_concatenation_plan(mgr, indexers):
    """
    Construct concatenation plan for given block manager and indexers.

    Parameters
    ----------
    mgr : BlockManager
    indexers : dict of {axis: indexer}

    Returns
    -------
    plan : list of (BlockPlacement, JoinUnit) tuples

    """
    # Calculate post-reindex shape , save for item axis which will be separate
    # for each block anyway.
    mgr_shape = list(mgr.shape)
    for ax, indexer in indexers.items():
        mgr_shape[ax] = len(indexer)
    mgr_shape = tuple(mgr_shape)

    if 0 in indexers:
        ax0_indexer = indexers.pop(0)
        blknos = com.take_1d(mgr._blknos, ax0_indexer, fill_value=-1)
        blklocs = com.take_1d(mgr._blklocs, ax0_indexer, fill_value=-1)
    else:

        if mgr._is_single_block:
            blk = mgr.blocks[0]
            return [(blk.mgr_locs, JoinUnit(blk, mgr_shape, indexers))]

        ax0_indexer = None
        blknos = mgr._blknos
        blklocs = mgr._blklocs

    plan = []
    for blkno, placements in _get_blkno_placements(blknos, len(mgr.blocks),
                                                   group=False):

        assert placements.is_slice_like

        join_unit_indexers = indexers.copy()

        shape = list(mgr_shape)
        shape[0] = len(placements)
        shape = tuple(shape)

        if blkno == -1:
            unit = JoinUnit(None, shape)
        else:
            blk = mgr.blocks[blkno]
            ax0_blk_indexer = blklocs[placements.indexer]

            unit_no_ax0_reindexing = (
                len(placements) == len(blk.mgr_locs) and
                # Fastpath detection of join unit not needing to reindex its
                # block: no ax0 reindexing took place and block placement was
                # sequential before.
                ((ax0_indexer is None
                  and blk.mgr_locs.is_slice_like
                  and blk.mgr_locs.as_slice.step == 1) or
                 # Slow-ish detection: all indexer locs are sequential (and
                 # length match is checked above).
                 (np.diff(ax0_blk_indexer) == 1).all()))

            # Omit indexer if no item reindexing is required.
            if unit_no_ax0_reindexing:
                join_unit_indexers.pop(0, None)
            else:
                join_unit_indexers[0] = ax0_blk_indexer

            unit = JoinUnit(blk, shape, join_unit_indexers)

        plan.append((placements, unit))

    return plan
