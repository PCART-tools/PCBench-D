def _reshard_output(
        module: torch.nn.Module,
        resharding_spec: ShardingSpec) -> torch.nn.Module:
    """
    Hook a module with local shards collection in the forward pass according
    to the given ``resharding_spec``.

    Args:
        module (:class:`torch.nn.Module`): Module whose output needs to be resharded.
        resharding_spec (:class:`torch.distributed._shard.sharding_spec.ShardingSpec`):
            The specification describing how the output of the module will be resharded.

    Returns:
        A :class:`torch.nn.Module` object with collection API hooked.
    """
    def hook_func(_module, _input, output):
        if isinstance(output, ShardedTensor) or isinstance(output, _PartialTensor):
            return output.reshard(resharding_spec)
        return output
    module.register_forward_hook(hook_func)
    return module
