def make_sharded_device_array(
    aval: ShapedArray,
    sharding_spec: Optional[ShardingSpec],
    # Any is for JAX extensions implementing their own buffer.
    device_buffers: List[Union[Any, xb.xla_client.Buffer]],
    indices: Optional[Tuple[Index, ...]] = None,
):
  """Returns a ShardedDeviceArray implementation based on arguments.

  Returns either a C++ SDA or a Python DeviceArray when the buffers are not
  JAX buffers.

  Args:
    aval: The `ShapedArray` for this array.
    sharding_spec: If `None`, assumes a pmap-style ShardedDeviceArrays over the
      first dimension.
    device_buffers: If a list of Jax `Buffer` objects, a C++ SDA will be
      returned (if the version is high enough). Otherwise, a Python object will
      be returned, for JAX extensions not implementing the C++ API.
    indices: For caching purposes, will be computed if `None`.
  """
  from jax._src import pjit

  if sharding_spec is None:
    sharding_spec = _create_pmap_sharding_spec(aval)

  mesh = jax._src.mesh.thread_resources.env.physical_mesh
  sharding: sharding_impls.XLACompatibleSharding
  if mesh.empty:
    sharding = sharding_impls.PmapSharding(
        np.asarray([d.device() for d in device_buffers]), sharding_spec)
  else:
    op_sharding = sharding_spec_sharding_proto(sharding_spec)
    pspec = pjit.parse_flatten_op_sharding(
        op_sharding, mesh)[0].get_partition_spec()
    sharding = sharding_impls.NamedSharding(mesh, pspec)

  return jax.make_array_from_single_device_arrays(
      aval.shape, sharding, device_buffers)  # type: ignore
