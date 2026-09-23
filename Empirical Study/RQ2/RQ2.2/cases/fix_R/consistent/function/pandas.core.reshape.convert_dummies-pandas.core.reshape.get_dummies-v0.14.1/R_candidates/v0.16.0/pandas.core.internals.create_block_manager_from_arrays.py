def create_block_manager_from_arrays(arrays, names, axes):
    try:
        blocks = form_blocks(arrays, names, axes)
        mgr = BlockManager(blocks, axes)
        mgr._consolidate_inplace()
        return mgr
    except (ValueError) as e:
        construction_error(len(arrays), arrays[0].shape, axes, e)
