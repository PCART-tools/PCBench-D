@contract(state_cls=FSDPState)  # type: ignore[misc] # see [1]
def fully_shard(
    module,
    *,
    mesh: Optional[DeviceMesh] = None,
    reshard_after_forward: Union[bool, int] = True,
    shard_placement_fn: Optional[Callable[[nn.Parameter], Optional[Shard]]] = None,
    mp_policy: MixedPrecisionPolicy = MixedPrecisionPolicy(),
    offload_policy: OffloadPolicy = OffloadPolicy(),
    ignored_params: Optional[set[nn.Parameter]] = None,
):
    """
    Apply fully sharded data parallelism (FSDP) to ``module``, where FSDP
    shards module parameters, gradients, and optimizer states across data
    parallel workers to save memory at the cost of communication.

    At initialization, FSDP shards the module's parameters across the data
    parallel workers given by ``mesh``. Before forward, FSDP all-gathers the
    sharded parameters across the data-parallel workers to get the unsharded
    parameters for forward computation. If ``reshard_after_forward`` is
    ``True``, then FSDP frees the unsharded parameters after forward and
    re-all-gathers them in backward before gradient computation. After gradient
    computation, FSDP frees the unsharded parameters and reduce-scatters the
    unsharded gradients across data-parallel workers.

    This implementation represents the sharded parameters as :class:`DTensor` s
    sharded on dim-0, while the unsharded parameters will be like the original
    parameters on ``module`` (e.g. :class:`torch.Tensor` if originally
    :class:`torch.Tensor`). A module
    `forward pre-hook <https://pytorch.org/docs/main/generated/torch.nn.Module.html#torch.nn.Module.register_forward_pre_hook>`_
    on ``module`` all-gathers the parameters, and a module
    `forward hook <https://pytorch.org/docs/main/generated/torch.nn.Module.html#torch.nn.Module.register_forward_hook>`_
    on ``module`` frees them (if needed). Similar backward hooks all-gather
    parameters and later free parameters and reduce-scatter gradients.

    Since grouping multiple tensors together for one collective is critical for
    communication efficiency, this implementation makes this grouping first
    class. Calling :meth:`fully_shard` on ``module`` constructs one group that
    includes the parameters in ``module.parameters()`` except those already
    assigned to a group from an earlier call on a submodule. This means that
    :meth:`fully_shard` should be called bottom-up on your model. Each group's
    parameters are all-gathered in one collective, and its gradients are
    reduce-scattered in one collective. Partitioning the model into multiple
    groups ("layer by layer") allows for peak memory savings and communication/computation
    overlap. Users generally should *not* call :meth:`fully_shard` only on the
    topmost root module.

    Args:
        module (Union[nn.Module, List[nn.Module]): The module or modules to
            shard with FSDP and group together for communication.
        mesh (Optional[DeviceMesh]): This data parallel mesh defines the
            sharding and device. If 1D, then parameters are fully sharded
            across the 1D mesh (FSDP) with ``(Shard(0),)`` placement. If 2D,
            then parameters are sharded across the 1st dim and replicated
            across the 0th dim (HSDP) with ``(Replicate(), Shard(0))``
            placement. The mesh's device type gives the device type used for
            communication; if a CUDA or CUDA-like device type, then we use the
            current device.
        reshard_after_forward (Union[bool, int]): This controls the parameter
            behavior after forward and can trade off memory and communication:

            - If ``True``, then this reshards parameters after forward and
              re-all-gathers in backward.
            - If ``False``, then this keeps the unsharded parameters in memory
              after forward and avoids the all-gather in backward.
            - If an ``int``, then this represents the world size to reshard to
              after forward. It should be a non-trivial divisor of the ``mesh``
              shard dim size (i.e. excluding 1 and the dim size itself). A
              choice may be the intra-node size (e.g. ``torch.cuda.device_count()``).
              This allows the all-gather in backward to be over a smaller world
              size at the cost of higher memory usage than setting to ``True``.
            - The root FSDP state has its value specially set to ``False`` as a
              heuristic since its parameters would typically be immediately
              all-gathered for backward.
            - After forward, the parameters registered to the module depend on
              to this: The registered parameters are the sharded parameters if
              ``True``; unsharded parameters if ``False``; and the paramters
              resharded to the smaller mesh otherwise. To modify the parameters
              between forward and backward, the registered parameters must be
              the sharded parameters. For ``False`` or an ``int``, this can be
              done by manually resharding via :meth:`reshard`.
        shard_placement_fn (Optional[Callable[[nn.Parameter], Optional[Shard]]]):
            This callable can be used to override the sharding placement for a
            parameter to shard a parameter on a dimension other than dim-0. If
            this callable returns a :class:`Shard` placement (not ``None``),
            then FSDP will shard according to that placement (e.g. ``Shard(1)``).
            If sharding on a nonzero dim, we currently require even sharding,
            i.e. the tensor dim size on that dim must be divisible by the FSDP
            shard mesh size.
        mp_policy (MixedPrecisionPolicy): This controls the mixed precision
            policy, which offers parameter/reduction mixed precision for this
            module. See :class:`MixedPrecisionPolicy` for details.
        offload_policy (OffloadPolicy): This controls the offloading policy,
            which offers parameter/gradient/optimizer state offloading. See
            :class:`OffloadPolicy` and its subclasses for details.
        ignored_params: Optional(Set[nn.Parameter]): The set of parameters that we
            don't want to shard with FSDP.

    Returns:
        FSDPModule: The module with FSDP applied (in-place).
    """
    if isinstance(module, (nn.ModuleList, nn.ModuleDict)):
        raise ValueError(
            f"fully_shard does not support containers that do not implement forward: {module}"
        )
    mesh = mesh or _init_default_fully_shard_mesh()
    if mesh.ndim not in (1, 2):
        raise ValueError(f"fully_shard expects a 1D or 2D DeviceMesh but got {mesh}")
    elif mesh.ndim == 1:
        mesh_info = FSDPMeshInfo(mesh, shard_mesh_dim=0)
    else:
        if mesh.mesh_dim_names is None:
            raise AssertionError(
                "Please init the 2D mesh for HSDP with mesh_dim_names specified"
            )
        mesh_info = HSDPMeshInfo(mesh, shard_mesh_dim=1, replicate_mesh_dim=0)
    device = _get_device_from_mesh(mesh)
    post_forward_mesh_info = _get_post_forward_mesh_info(
        reshard_after_forward, mesh_info
    )

    arg_module = module
    modules = (
        (module,) if isinstance(module, nn.Module) else tuple(_get_root_modules(module))
    )
    state = fully_shard.state(modules[0])  # type: ignore[attr-defined] # see [1]
    state.init(modules, device, mp_policy)

    managed_modules = _get_managed_modules(modules, ignored_params)
    params, buffers = _get_managed_states(managed_modules, ignored_params)

    _move_states_to_device(params, buffers, device)
    if params:
        state._fsdp_param_group = FSDPParamGroup(
            params,
            modules,
            mesh_info,
            post_forward_mesh_info,
            device,
            shard_placement_fn,
            mp_policy,
            offload_policy,
        )

    # For Dynamo
    for managed_module in managed_modules:
        managed_module._is_fsdp_managed_module = True  # type: ignore[assignment]
        managed_module._fsdp_use_orig_params = True  # type: ignore[assignment]

    # Place FSDP leftmost for highest priority in the method resolution order
    for module in modules:
        cls = module.__class__
        new_cls = cls_to_fsdp_cls.get(cls, None)
        if not new_cls:
            dct = {"__deepcopy__": _unimplemented_deepcopy}
            new_cls = type(f"FSDP{cls.__name__}", (FSDPModule, cls), dct)
            cls_to_fsdp_cls[cls] = new_cls
        module.__class__ = new_cls
    return arg_module
