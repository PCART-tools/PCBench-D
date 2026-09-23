def concatenate_block_managers(mgrs_indexers, axes, concat_axis, copy):
    """
    Concatenate block managers into one.

    Parameters
    ----------
    mgrs_indexers : list of (BlockManager, {axis: indexer,...}) tuples
    axes : list of Index
    concat_axis : int
    copy : bool

    """
    concat_plan = combine_concat_plans([get_mgr_concatenation_plan(mgr, indexers)
                                        for mgr, indexers in mgrs_indexers],
                                       concat_axis)

    blocks = [make_block(concatenate_join_units(join_units, concat_axis,
                                                copy=copy),
                         placement=placement)
              for placement, join_units in concat_plan]

    return BlockManager(blocks, axes)
