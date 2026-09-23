def _dtensor_init_helper(  # type: ignore[no-untyped-def]
    init_op,
    size: torch.Size,
    device_mesh: Optional[DeviceMesh] = None,
    placements: Optional[Sequence[Placement]] = None,
    **kwargs,
) -> DTensor:
    # from torch.distributed._tensor.placement_types import DTensorSpec, TensorMeta

    # if device_mesh is None, use the one from mesh resources
    device_mesh = device_mesh or _mesh_resources.get_current_mesh()
    kwargs["device"] = device_mesh.device_type

    # set default placements to replicated if not specified
    placements = placements or tuple(Replicate() for _ in range(device_mesh.ndim))

    # check device_mesh againts placements
    assert device_mesh.ndim == len(placements), (
        "mesh dimension does not match the length of placements"
    )

    assert kwargs["layout"] == torch.strided, "layout value not supported!"
    torch_stride = torch._prims_common.make_contiguous_strides_for(size)

    # get local tensor shape
    local_shape, _ = compute_local_shape_and_global_offset(
        size, device_mesh, placements
    )

    # initialize the local tensor
    if init_op == torch.full:
        fill_value = kwargs.pop("fill_value", 0)
        local_tensor = init_op(local_shape, fill_value, **kwargs)
    elif init_op == torch.rand or init_op == torch.randn:
        # this tensor meta is not used except `shape`
        dtype = kwargs.get("dtype", torch.get_default_dtype())

        tensor_meta = TensorMeta(size, (0,), dtype)
        spec = DTensorSpec(device_mesh, tuple(placements), tensor_meta=tensor_meta)

        if random.is_rng_supported_mesh(device_mesh) and not random._rng_tracker:
            random._rng_tracker = random.OffsetBasedRNGTracker(device_mesh)

        assert random._rng_tracker is not None
        with random._rng_tracker._distribute_region(spec):
            local_tensor = init_op(local_shape, **kwargs)
    else:
        local_tensor = init_op(local_shape, **kwargs)

    spec = DTensorSpec(
        device_mesh,
        tuple(placements),
        tensor_meta=TensorMeta(
            size,
            torch_stride,
            local_tensor.dtype,
        ),
    )

    return DTensor(
        local_tensor,
        spec,
        requires_grad=kwargs["requires_grad"],
    )
