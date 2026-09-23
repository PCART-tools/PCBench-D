    @torch.library.register_fake("_dtensor::shard_dim_alltoall")
    def _shard_dim_alltoall_meta(input, gather_dim, shard_dim, group_name):
        group_size = _get_group_size_by_name(group_name)
        stacked_list = [torch.empty_like(input) for _ in range(group_size)]
        group = _resolve_process_group(group_name)
        group_rank = get_group_rank(group, get_rank())

        return (
            torch.cat(stacked_list, dim=gather_dim)
            .chunk(group_size, dim=shard_dim)[group_rank]
            .contiguous()
        )
