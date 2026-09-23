  @staticmethod
  def global_sharded_result_handler(aval, out_sharding, committed):
    phys_aval = core.physical_aval(aval)
    phys_handler_maker = pxla.global_result_handlers[core.ShapedArray]

    if not dispatch.is_single_device_sharding(out_sharding):
      raise NotImplementedError  # TODO(mattjj)
    else:
      phys_sharding = out_sharding
    phys_handler = phys_handler_maker(phys_aval, phys_sharding, committed)

    def handler(bufs):
      return core.DArray(aval, phys_handler(bufs))
    return handler
