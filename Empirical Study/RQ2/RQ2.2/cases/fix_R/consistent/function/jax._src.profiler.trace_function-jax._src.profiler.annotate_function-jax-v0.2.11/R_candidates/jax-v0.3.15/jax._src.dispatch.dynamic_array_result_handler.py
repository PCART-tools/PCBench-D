def dynamic_array_result_handler(sticky_device: Optional[Device],
                                 aval: core.DShapedArray):
  if aval.dtype == dtypes.float0:
    return lambda _: np.zeros(aval.shape, dtypes.float0)  # type: ignore
  else:
    return partial(_dynamic_array_result_handler, sticky_device, aval)
