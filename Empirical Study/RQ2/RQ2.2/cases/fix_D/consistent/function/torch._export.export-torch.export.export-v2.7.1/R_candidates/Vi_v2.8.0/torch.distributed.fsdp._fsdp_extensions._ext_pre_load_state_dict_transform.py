def _ext_pre_load_state_dict_transform(
    tensor: torch.Tensor,
    fsdp_extension: Optional[FSDPExtensions] = None,
) -> tuple[torch.Tensor, list[Shard]]:
    if fsdp_extension is not None:
        return fsdp_extension.pre_load_state_dict_transform(tensor)

    assert type(tensor) is ShardedTensor
    shards = tensor.local_shards()
    return (tensor, shards)
