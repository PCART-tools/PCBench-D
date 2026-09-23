def _validate_linear_op_param(args, kwargs):
    """
    Validate input params of sharded embedding op.

    Args:
        input: input of the linear layer.
        weight: shareded weight tensor.
        kwargs: same as normal Linear.

    Return: None.
    """
    input = args[0]
    weight = args[1]
    bias = args[2]

    # Validate types
    if not isinstance(input, torch.Tensor) and not isinstance(input, ShardedTensor):
        raise TypeError("input needs to be either torch.Tensor or ShardedTensor")
    if not isinstance(bias, torch.Tensor):
        raise TypeError("bias needs to be torch.Tensor")
    if not isinstance(weight, ShardedTensor):
        raise TypeError("weight needs to be ShardedTensor")
    if len(input.size()) < 1:  # type: ignore[arg-type]
        raise ValueError("Input needs to have at least 1 dim")
    weight_size = cast(torch.Size, weight.size())
    if len(weight_size) != 2:
        raise ValueError("Weight needs to have exactly 2 dims")
    if len(bias.size()) != 1:
        raise ValueError("Bias needs to have exactly 1 dim")
    if input.size()[-1] != weight_size[1]:  # type: ignore[index]
        raise ValueError(
            f"Input dim: {input.size()[-1]} does not match "  # type: ignore[index]
            f"appropriate weight dim: {weight_size[1]}"
        )
    if not isinstance(weight._sharding_spec, ChunkShardingSpec):
        raise ValueError("Only ChunkShardingSpec supported for ShardedTensor ops!")
    if len(weight.local_shards()) != 1:
        raise ValueError("Only one local shard supported!")
