def manual_seed(seed: int, device_mesh: DeviceMesh) -> None:
    """Sets the seed for generating random numbers for the calling rank.

    Args:
        seed (int): The desired seed.
        device_mesh (:class:`DeviceMesh`): The device mesh to set the seed. It is
            required that the ``device_mesh`` include the calling rank. This is
            to ensure that the SPMD region maintains a synchronous RNG state, which
            means no ranks should be initialized with values other than ``seed``.

    Returns:
        None

    .. warning::
        :func:`manual_seed` does not check the ``seed`` value correctness. Users must
        ensure on their own that the value passed in is the desired ``seed`` for ranks
        within ``device_mesh``.
        If ``device_mesh`` is a sub-mesh and the calling rank is not a part of it,
        ``manual_seed`` will throw an error.
        Current implementation only supports a GPU device mesh.
    """
    if not is_rng_supported_mesh(device_mesh):
        warnings.warn(
            "DTensor manual_seed() may not have complete support "
            f"on {device_mesh.device_type} device mesh"
        )
        return

    # instantiate a RNG tracker if haven't. By default DTensor uses an
    # OffsetBasedRNGTracker to perform random operators.
    global _rng_tracker
    if not _rng_tracker:
        _rng_tracker = OffsetBasedRNGTracker(device_mesh, run_state_sync=False)

    # the current rank is in mesh
    if device_mesh.get_coordinate() is not None:
        _rng_tracker._manual_seed(seed)
    else:
        raise RuntimeError(
            "manual_seed requires the current rank to be a part of the device mesh "
            "otherwise DTensor RNG state on the rank will not be initialized and "
            "the behavior of DTensor random ops is undefined."
        )
