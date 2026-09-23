def get_compile_options(
    num_replicas: int,
    num_partitions: int,
    device_assignment=None,
    use_spmd_partitioning: bool = True,
    use_auto_spmd_partitioning: bool = False,
    auto_spmd_partitioning_mesh_shape=[],
    auto_spmd_partitioning_mesh_ids=[],
    env_options_overrides: Optional[dict[str, str]] = None,
    fdo_profile: Optional[bytes] = None,
) -> xla_client.CompileOptions:
  """Returns the compile options to use, as derived from flag values.

  Args:
    num_replicas: Number of replicas for which to compile.
    num_partitions: Number of partitions for which to compile.
    device_assignment: Optional ndarray of jax devices indicating the assignment
      of logical replicas to physical devices (default inherited from
      xla_client.CompileOptions). Must be consistent with `num_replicas` and
      `num_partitions`.
    use_spmd_partitioning: boolean indicating whether to enable SPMD or MPMD
      partitioning in XLA.
    use_auto_spmd_partitioning: boolean indicating whether to automatically
      generate XLA shardings for SPMD partitioner.
    auto_spmd_partitioning_mesh_shape: device mesh shape used to create
      auto_spmd_partitioning search space.
    auto_spmd_partitioning_mesh_ids: device ids used to create
      auto_spmd_partitioning search space.
    env_options_overrides: dict of additional options parsed by the compiler
    fdo_profile: Optional profile for feedback-directed optimization passed to
    XLA.
  """
  compile_options = xla_client.CompileOptions()
  compile_options.num_replicas = num_replicas
  compile_options.num_partitions = num_partitions
  build_options = compile_options.executable_build_options
  build_options.use_spmd_partitioning = use_spmd_partitioning
  build_options.use_auto_spmd_partitioning = use_auto_spmd_partitioning
  if xla_extension_version > 165 and fdo_profile is not None:
    build_options.fdo_profile = fdo_profile
  if use_auto_spmd_partitioning:
    build_options.auto_spmd_partitioning_mesh_shape = auto_spmd_partitioning_mesh_shape
    build_options.auto_spmd_partitioning_mesh_ids = auto_spmd_partitioning_mesh_ids
  if device_assignment is not None:
    logger.debug(
        'get_compile_options: num_replicas=%s num_partitions=%s device_assignment=%s',
        num_replicas, num_partitions, device_assignment)
    device_assignment = np.array(device_assignment)

    # Allow 1D device assignment if num_partitions is 1.
    if (device_assignment.ndim == 1) and (num_partitions == 1):
      device_assignment = device_assignment[:, None]

    if num_replicas != device_assignment.shape[0]:
      msg = 'device_assignment does not match num_replicas: {} vs {}.'
      raise ValueError(msg.format(device_assignment, num_replicas))

    if num_partitions != device_assignment.shape[1]:
      msg = 'device_assignment does not match num_partitions: {} vs {}.'
      raise ValueError(msg.format(device_assignment, num_partitions))

    if device_assignment.dtype == object:
      device_assignment = np.vectorize(lambda d: d.id, otypes=[int])(
          device_assignment)
    device_assignment = xla_client.DeviceAssignment.create(device_assignment)
    assert device_assignment.replica_count() == num_replicas
    assert device_assignment.computation_count() == num_partitions
    compile_options.device_assignment = device_assignment

  if env_options_overrides is not None:
    compile_options.env_option_overrides = list(env_options_overrides.items())

  debug_options = compile_options.executable_build_options.debug_options
  if lib.cuda_path is not None:
    debug_options.xla_gpu_cuda_data_dir = lib.cuda_path

  if _DISABLE_MOST_OPTIMIZATIONS.value:

    debug_options.xla_backend_optimization_level = 0
    debug_options.xla_llvm_disable_expensive_passes = True
    debug_options.xla_test_all_input_layouts = False

  compile_options.profile_version = _XLA_PROFILE_VERSION.value
  return compile_options
