def _unstack_frame(obj, level):
    from pandas.core.internals import BlockManager, make_block

    if obj._is_mixed_type:
        unstacker = _Unstacker(np.empty(obj.shape, dtype=bool),  # dummy
                               obj.index, level=level,
                               value_columns=obj.columns)
        new_columns = unstacker.get_new_columns()
        new_index = unstacker.get_new_index()
        new_axes = [new_columns, new_index]

        new_blocks = []
        mask_blocks = []
        for blk in obj._data.blocks:
            blk_items = obj._data.items[blk.mgr_locs.indexer]
            bunstacker = _Unstacker(blk.values.T, obj.index, level=level,
                                    value_columns=blk_items)
            new_items = bunstacker.get_new_columns()
            new_placement = new_columns.get_indexer(new_items)
            new_values, mask = bunstacker.get_new_values()

            mblk = make_block(mask.T, placement=new_placement)
            mask_blocks.append(mblk)

            newb = make_block(new_values.T, placement=new_placement)
            new_blocks.append(newb)

        result = DataFrame(BlockManager(new_blocks, new_axes))
        mask_frame = DataFrame(BlockManager(mask_blocks, new_axes))
        return result.ix[:, mask_frame.sum(0) > 0]
    else:
        unstacker = _Unstacker(obj.values, obj.index, level=level,
                               value_columns=obj.columns)
        return unstacker.get_result()
