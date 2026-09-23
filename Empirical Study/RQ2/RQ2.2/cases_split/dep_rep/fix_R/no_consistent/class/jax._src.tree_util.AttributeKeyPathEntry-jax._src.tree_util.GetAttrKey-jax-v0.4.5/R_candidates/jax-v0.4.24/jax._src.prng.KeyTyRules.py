class KeyTyRules:

  @staticmethod
  def full(shape, fill_value, dtype):
    physical_shape = (*shape, *dtype._impl.key_shape)
    if hasattr(fill_value, 'dtype') and jnp.issubdtype(fill_value.dtype, dtypes.prng_key):
      key_data = jnp.broadcast_to(random_unwrap(fill_value), physical_shape)
    else:
      key_data = lax.full(physical_shape, fill_value, dtype=np.dtype('uint32'))
    # TODO(frostig,mattjj,vanderplas,lenamartens): consider this consumed from
    # the outset.
    return random_wrap(key_data, impl=dtype._impl)

  @staticmethod
  def physical_element_aval(dtype) -> core.ShapedArray:
    return core.ShapedArray(dtype._impl.key_shape, jnp.dtype('uint32'))

  @staticmethod
  def physical_const(val) -> Array:
    return val._base_array

  @staticmethod
  def physical_hlo_sharding(aval, hlo_sharding: xc.HloSharding) -> xc.HloSharding:
    key_shape = aval.dtype._impl.key_shape
    op_sharding_proto = hlo_sharding.to_proto()  # type: ignore
    new_op_sharding = op_sharding_proto.clone()
    tad = list(new_op_sharding.tile_assignment_dimensions)
    suffix = [tad.pop()] if op_sharding_proto.replicate_on_last_tile_dim else []
    tad.extend([1] * len(key_shape) + suffix)
    new_op_sharding.tile_assignment_dimensions = tad
    return xc.HloSharding.from_proto(new_op_sharding)

  @staticmethod
  def logical_op_sharding(aval, phys_sharding) -> XLACompatibleSharding:
    if dispatch.is_single_device_sharding(phys_sharding):
      return phys_sharding
    elif isinstance(phys_sharding, PmapSharding):
      key_shape = aval.dtype._impl.key_shape
      logical_sharding_spec = sharding_specs.ShardingSpec(
          sharding=phys_sharding.sharding_spec.sharding[:-len(key_shape)],
          mesh_mapping=phys_sharding.sharding_spec.mesh_mapping)
      return PmapSharding(devices=phys_sharding.devices,
                          sharding_spec=logical_sharding_spec)
    elif isinstance(phys_sharding, NamedSharding):
      key_shape = aval.dtype._impl.key_shape
      return pxla.create_mesh_pspec_sharding(
          phys_sharding.mesh,
          PartitionSpec(*phys_sharding.spec[:-len(key_shape)]))
    else:
      key_shape = aval.dtype._impl.key_shape
      phys_op_sharding = phys_sharding._to_xla_hlo_sharding(
          aval.ndim + len(key_shape)).to_proto()
      logical_op_sharding = phys_op_sharding.clone()
      tad = list(logical_op_sharding.tile_assignment_dimensions)
      tad = tad[:-len(key_shape)]
      logical_op_sharding.tile_assignment_dimensions = tad
      return GSPMDSharding(phys_sharding._device_assignment,
                           xc.HloSharding.from_proto(logical_op_sharding))

  @staticmethod
  def result_handler(sticky_device, aval):
    def handler(_, buf):
      buf.aval = core.ShapedArray(buf.shape, buf.dtype)
      return PRNGKeyArray(aval.dtype._impl, buf)
    return handler

  @staticmethod
  def local_sharded_result_handler(aval, sharding, indices):
    phys_aval = core.physical_aval(aval)
    key_shape = aval.dtype._impl.key_shape
    phys_handler_maker = pxla.local_result_handlers[core.ShapedArray]

    # set up a grounded sharding (with a grounded sharding spec)
    if isinstance(sharding, (PmapSharding, NamedSharding)):
      phys_sharding = make_key_array_phys_sharding(
          aval, sharding, is_sharding_from_xla=False)
    else:
      assert False, f'impossible sharding {sharding} in local sharded result handler'

    # set up grounded indices
    trailing_inds = [slice(None)] * len(key_shape)
    phys_indices = [(*inds, *trailing_inds) for inds in indices]

    # make a physical handler
    phys_handler = phys_handler_maker(phys_aval, phys_sharding, phys_indices)

    # set up a handler that calls the physical one and wraps back up
    def handler(bufs):
      return PRNGKeyArray(aval.dtype._impl, phys_handler(bufs))

    return handler

  @staticmethod
  def global_sharded_result_handler(aval, out_sharding, committed,
                                    is_out_sharding_from_xla):
    phys_aval = core.physical_aval(aval)
    phys_handler_maker = pxla.global_result_handlers[core.ShapedArray]

    phys_sharding = make_key_array_phys_sharding(
        aval, out_sharding, is_out_sharding_from_xla)
    phys_handler = phys_handler_maker(phys_aval, phys_sharding, committed,
                                      is_out_sharding_from_xla)
    def handler(bufs):
      return PRNGKeyArray(aval.dtype._impl, phys_handler(bufs))
    return handler

  @staticmethod
  def make_sharded_array(aval, sharding, arrays, committed):
    phys_aval = core.physical_aval(aval)
    phys_handler_maker = pxla.global_result_handlers[core.ShapedArray]
    phys_arrays = [random_unwrap(arr) for arr in arrays]

    phys_sharding = make_key_array_phys_sharding(aval, sharding, False)
    phys_handler = phys_handler_maker(phys_aval, phys_sharding, committed, False)
    phys_result = phys_handler(phys_arrays)
    return PRNGKeyArray(aval.dtype._impl, phys_result)

  @staticmethod
  def device_put_sharded(vals, aval, sharding, devices):
    physical_aval = core.physical_aval(aval)
    physical_buffers = tree_util.tree_map(random_unwrap, vals)
    physical_sharding = make_key_array_phys_sharding(aval, sharding, False)
    physical_result = pxla.batched_device_put(physical_aval, physical_sharding, physical_buffers, list(devices))
    return random_wrap(physical_result, impl=aval.dtype._impl)

  @staticmethod
  def device_put_replicated(val, aval, sharding, devices):
    physical_aval = core.physical_aval(aval)
    assert len(xla.aval_to_xla_shapes(physical_aval)) == 1
    physical_buf = random_unwrap(val)
    physical_sharding = make_key_array_phys_sharding(aval, sharding, False)
    physical_result = pxla.batched_device_put(physical_aval, physical_sharding, [physical_buf] * len(devices), devices)
    return random_wrap(physical_result, impl=aval.dtype._impl)

  @staticmethod
  def tangent_dtype(_):
    return dtypes.float0

  # TODO(mattjj,frostig): even though the key dtype shouldn't appear in
  # tangents, our ad.replace_float0s in custom_jvp/vjp means passing in zeros
  # like the primal to user rules
  @staticmethod
  def zero(_):
    return np.zeros((), dtypes.float0)

  @staticmethod
  def convert_from(key_dtype, other_dtype) -> bool:
    return False

  @staticmethod
  def convert_to(other_dtype, key_dtype) -> bool:
    return False
