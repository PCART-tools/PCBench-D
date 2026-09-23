  @staticmethod
  def local_sharded_result_handler(aval, sharding, indices):
    phys_aval = core.physical_aval(aval)
    key_shape = aval.dtype._impl.key_shape
    phys_handler_maker = pxla.local_result_handlers[core.ShapedArray]

    # set up a grounded sharding (with a grounded sharding spec)
    if isinstance(sharding, (PmapSharding, NamedSharding)):
      phys_sharding = make_key_array_phys_sharding(aval, sharding)
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
