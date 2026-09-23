def _collect_local_shard(module: torch.nn.Module) -> torch.nn.Module:
    """
    Hook a module with local shards collection in the forward pass.

    This API is typically used to convert a sharded representation back to data parallel
    representation. In particular, it returns the local tensor for this Shard. If the
    size along the sharding dimension for the local tensor is 1, this dimension is removed
    from the final result. For example a [4, 16] ShardedTensor across 4 ranks is typically
    a local Tensor of size [16] across each rank and not [1, 16] across each rank.

    Args:
        module (:class:`torch.nn.Module`): Module whose output needs to be resharded.

    Returns:
        A :class:`torch.nn.Module` object with collection API hooked.
    """

    def hook_func(_module, _input, output):
        if isinstance(output, ShardedTensor):
            local_tensor = output.local_tensor()
            # Squeeze the # of dimensions manually.
            if local_tensor.size(output._sharding_spec.dim) == 1:  # type: ignore[attr-defined]
                local_tensor = local_tensor.squeeze(
                    output._sharding_spec.dim  # type: ignore[attr-defined]
                )
            return local_tensor
    module.register_forward_hook(hook_func)
    return module
