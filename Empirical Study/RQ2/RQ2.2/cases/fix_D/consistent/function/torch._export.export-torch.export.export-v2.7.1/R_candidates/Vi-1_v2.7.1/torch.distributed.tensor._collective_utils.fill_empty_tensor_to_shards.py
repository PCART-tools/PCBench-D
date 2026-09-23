def fill_empty_tensor_to_shards(
    shards: list[torch.Tensor], shard_dim: int, num_empty_tensors: int
) -> list[torch.Tensor]:
    if num_empty_tensors == 0:
        return shards
    tensor_size = list(shards[0].size())
    tensor_size = [
        size if idx != shard_dim else 0 for idx, size in enumerate(tensor_size)
    ]
    tensor = shards[0].new_zeros(tensor_size)
    shards.extend(tensor for _ in range(num_empty_tensors))
    return shards
