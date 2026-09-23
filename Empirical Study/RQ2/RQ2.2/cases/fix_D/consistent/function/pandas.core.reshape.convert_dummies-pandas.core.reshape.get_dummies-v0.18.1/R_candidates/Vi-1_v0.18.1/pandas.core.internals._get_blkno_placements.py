def _get_blkno_placements(blknos, blk_count, group=True):
    """

    Parameters
    ----------
    blknos : array of int64
    blk_count : int
    group : bool

    Returns
    -------
    iterator
        yield (BlockPlacement, blkno)

    """

    blknos = com._ensure_int64(blknos)

    # FIXME: blk_count is unused, but it may avoid the use of dicts in cython
    for blkno, indexer in lib.get_blkno_indexers(blknos, group):
        yield blkno, BlockPlacement(indexer)
