def _all_gather_into_tensor_coalesced_meta(self, tag, rankset, group_size):
    def mk_out_tensor(shard):
        out_size = list(shard.size())
        out_size[0] *= group_size
        out_tensor = shard.new_empty(out_size)
        return out_tensor

    return [mk_out_tensor(t) for t in self]
