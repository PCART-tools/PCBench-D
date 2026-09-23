  @staticmethod
  def make_sharded_array(aval, sharding, arrays, committed):
    phys_aval = core.physical_aval(aval)
    phys_handler_maker = pxla.global_result_handlers[core.ShapedArray]
    phys_arrays = [random_unwrap(arr) for arr in arrays]

    phys_sharding = make_key_array_phys_sharding(aval, sharding)
    phys_handler = phys_handler_maker(phys_aval, phys_sharding, committed)
    phys_result = phys_handler(phys_arrays)
    return PRNGKeyArray(aval.dtype._impl, phys_result)
