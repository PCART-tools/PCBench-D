@contract(state_cls=_ReplicateState)
def replicate(
    module: nn.Module,
    ignored_modules: Optional[Iterable[torch.nn.Module]] = None,
    **kwargs,
) -> nn.Module:
    r"""Replicates a module

    Args:
        module (torch.nn.Module): module to replicate

    Example::
        >>> # xdoctest: +REQUIRES(module:torch._C._distributed_c10d)
        >>> module = nn.Linear(3, 3)
        >>> replicate(module)
    """
    torch._C._log_api_usage_once("torch.distributed.replicate")

    # TODO(fegin): using kwargs is not a good idea if we would like to make
    # replicate a formal API to replace DDP.
    if "device_id" in kwargs:
        if not isinstance(kwargs["device_id"], (int, torch.device)):
            raise RuntimeError(
                "Expected device_id to be int or torch.device, "
                f"but got {type(kwargs['device_id'])}"
            )

    if _is_fully_sharded(module):
        raise RuntimeError(
            "Cannot apply `replicate()` on a Module already managed by `fully_shard`"
        )

    if ignored_modules is None:
        ignored_modules = {}
    else:
        ignored_modules = set(ignored_modules)

    state = replicate.state(module)
    module.register_forward_pre_hook(state.forward_pre_hook, with_kwargs=True)
    device_mesh = kwargs.get("device_mesh", None)
    if device_mesh is not None:
        from torch.distributed.device_mesh import _mesh_resources

        root_mesh = _mesh_resources.get_root_mesh(device_mesh)
        # if a root mesh is not the same as device_mesh,
        # meaning the device_mesh is sliced out from the root mesh.
        if root_mesh != device_mesh:
            # TODO: This is a temporary work around to enable DDP + TP.
            # We should do the logic in DDP so that the 2D implementation is
            # sound and the state_dict works out of the box.
            #
            # This won't conflict with what is done in DDP class as the module
            # replicate is going to pass is NOT the original module.
            from torch.distributed.tensor.parallel.ddp import (
                _localize_dtensor,
                _reconstruct_dtensor,
            )

            module.register_forward_pre_hook(_reconstruct_dtensor)
            module.register_forward_hook(_localize_dtensor)

    module.register_forward_hook(state.forward_post_hook)  # type: ignore[arg-type]

    state.record_init_args(module, ignored_modules, **kwargs)

    # Place DDP leftmost for highest priority in the method resolution order
    cls = module.__class__
    dct = {"__deepcopy__": unimplemented_deepcopy}
    new_cls = type(f"DDP{cls.__name__}", (DDP, cls), dct)
    module.__class__ = new_cls
    return module
