def create_block_manager_from_blocks(blocks, axes):
    try:
        if len(blocks) == 1 and not isinstance(blocks[0], Block):
            # It's OK if a single block is passed as values, its placement is
            # basically "all items", but if there're many, don't bother
            # converting, it's an error anyway.
            blocks = [make_block(values=blocks[0],
                                 placement=slice(0, len(axes[0])))]

        mgr = BlockManager(blocks, axes)
        mgr._consolidate_inplace()
        return mgr

    except (ValueError) as e:
        blocks = [getattr(b, 'values', b) for b in blocks]
        tot_items = sum(b.shape[0] for b in blocks)
        construction_error(tot_items, blocks[0].shape[1:], axes, e)
