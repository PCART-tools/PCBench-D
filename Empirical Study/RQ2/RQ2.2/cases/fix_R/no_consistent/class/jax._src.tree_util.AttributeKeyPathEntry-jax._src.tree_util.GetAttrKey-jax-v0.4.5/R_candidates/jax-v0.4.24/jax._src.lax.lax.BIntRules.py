class BIntRules:
  @staticmethod
  def physical_element_aval(dtype) -> core.ShapedArray:
    return core.ShapedArray((), np.dtype('int32'))

  @staticmethod
  def result_handler(sticky_device, aval):
    def handler(_, buf):
      buf.aval = core.ShapedArray(buf.shape, buf.dtype)
      return core.DArray(aval, buf)
    return handler

  @staticmethod
  def global_sharded_result_handler(aval, out_sharding, committed,
                                    is_out_sharding_from_xla):
    phys_aval = core.physical_aval(aval)
    phys_handler_maker = pxla.global_result_handlers[core.ShapedArray]

    if not dispatch.is_single_device_sharding(out_sharding):
      raise NotImplementedError  # TODO(mattjj)
    else:
      phys_sharding = out_sharding
    phys_handler = phys_handler_maker(phys_aval, phys_sharding, committed,
                                      is_out_sharding_from_xla)

    def handler(bufs):
      return core.DArray(aval, phys_handler(bufs))
    return handler

  @staticmethod
  def physical_hlo_sharding(aval, hlo_sharding: xc.HloSharding) -> xc.HloSharding:
    return hlo_sharding

  @staticmethod
  def convert_from(bint_dtype, other_dtype) -> bool:
    return other_dtype in (np.dtype('int32'), np.dtype('int64'))

  @staticmethod
  def convert_to(other_dtype, bint_dtype) -> bool:
    return other_dtype in (np.dtype('int32'), np.dtype('int64'))
