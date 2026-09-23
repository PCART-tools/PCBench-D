def trim_join_unit(join_unit, length):
    """
    Reduce join_unit's shape along item axis to length.

    Extra items that didn't fit are returned as a separate block.
    """

    if 0 not in join_unit.indexers:
        extra_indexers = join_unit.indexers

        if join_unit.block is None:
            extra_block = None
        else:
            extra_block = join_unit.block.getitem_block(slice(length, None))
            join_unit.block = join_unit.block.getitem_block(slice(length))
    else:
        extra_block = join_unit.block

        extra_indexers = copy.copy(join_unit.indexers)
        extra_indexers[0] = extra_indexers[0][length:]
        join_unit.indexers[0] = join_unit.indexers[0][:length]

    extra_shape = (join_unit.shape[0] - length,) + join_unit.shape[1:]
    join_unit.shape = (length,) + join_unit.shape[1:]

    return JoinUnit(block=extra_block, indexers=extra_indexers,
                    shape=extra_shape)
