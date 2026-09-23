def _all_gather_into_tensor_meta(shard, tag, rankset, group_size):
    out_size = list(shard.size())
    out_size[0] *= group_size
    return shard.new_empty(out_size)
