def checkpoint_wrapper(
    module: torch.nn.Module,
    checkpoint_impl: CheckpointImpl = CheckpointImpl.REENTRANT,
    offload_to_cpu: bool = False,
) -> torch.nn.Module:
    """
    A convenience wrapper for activation checkpointing. If the module is wrapped
    with this function, all subsequent calls to the module will automatically
    perform checkpointing without the user having to explicitly call ``checkpoint``
    function.
    Usage::
        checkpointed_module = checkpoint_wrapper(module)
        outputs = checkpointed_module(inputs)
    Args:
        module (nn.Module):
            The module to be wrapped
        checkpoint_impl (Optional[CheckpointImpl]):
            The checkpointing implementation to use. Currently only
            CheckpointImpl.REENTRANT is supported.
        offload_to_cpu (Optional[bool]):
            Whether to offload outer activations to CPU. Note that this
            currently only works with CheckpointImpl.REENTRANT.

    Returns:
        (nn.Module):
            Wrapped module
    """
    # saved tensor hooks based-checkpoint wrapper is not yet supported.
    if checkpoint_impl == CheckpointImpl.NO_REENTRANT:
        raise ValueError(
            "No support for non-reentrant based checkpoint implementation."
        )

    if offload_to_cpu and checkpoint_impl != CheckpointImpl.REENTRANT:
        raise ValueError(
            "No support for CPU offload activations and non-reentrant based "
            "checkpoint implementation."
        )

    return _CheckpointWrapper(module, checkpoint_impl, offload_to_cpu)
