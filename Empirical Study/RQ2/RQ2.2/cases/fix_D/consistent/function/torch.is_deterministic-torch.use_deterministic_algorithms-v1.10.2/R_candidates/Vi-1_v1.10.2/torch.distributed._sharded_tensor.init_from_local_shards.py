def init_from_local_shards(
        local_shards: List[Shard],
        sharded_tensor_metadata: ShardedTensorMetadata,
        process_group=None,
        init_rrefs=False):
    """
    Creates an :class:`ShardedTensor` from local shards and the global metadata.
    Needs to be called on all ranks in an SPMD fashion.

    Args:
        local_shards (List[:class `torch.distributed._sharded_tensor.Shard`]): A list
            of shards that represent the local shards on this rank.
        sharded_tensor_metadata (:class:`torch.distributed._sharded_tensor.ShardedTensorMetadata`)
            The ShardedTensorMetadata that created manually, represents the global metadata
            of the ShardedTensor, must comply with `local_shards` defined in each rank.
            Note that `sharded_tensor_metadata` must be valid and should also contain
            local shards metadata.

    Keyword args:
        process_group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        init_rrefs (bool, optional): Whether or not to initialize
            :class:`torch.distributed.rpc.RRef`s pointing to remote shards.
            Need to initialize the RPC Framework if specified as ``True``.
            Default: ``False``.

    Returns:
        A :class:`ShardedTensor` object handle on this rank
    """
    return ShardedTensor._init_from_local_shards(
        local_shards,
        sharded_tensor_metadata,
        process_group=process_group,
        init_rrefs=init_rrefs
    )
