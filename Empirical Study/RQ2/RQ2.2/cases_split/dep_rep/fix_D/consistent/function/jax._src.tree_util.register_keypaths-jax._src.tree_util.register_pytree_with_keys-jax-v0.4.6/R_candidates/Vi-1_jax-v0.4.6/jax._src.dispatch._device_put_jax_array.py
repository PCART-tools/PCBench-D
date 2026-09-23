def _device_put_jax_array(x, device: Optional[Device]):
  if is_single_device_sharding(x.sharding):
    x = _copy_device_array_to_device(_set_aval(x._arrays[0]), device)
    return (x,)
  else:
    # Round trip via host if x is sharded. SDA also does a round trip via host.
    return _device_put_array(x._value, device)
