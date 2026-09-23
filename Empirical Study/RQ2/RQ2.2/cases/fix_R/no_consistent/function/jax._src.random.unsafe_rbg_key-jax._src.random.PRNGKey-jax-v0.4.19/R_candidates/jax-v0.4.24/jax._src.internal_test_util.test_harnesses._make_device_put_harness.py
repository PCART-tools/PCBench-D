def _make_device_put_harness(name,
                             *,
                             shape=(3, 4),
                             dtype=np.float32,
                             device=None):
  _device_fn = lambda: jax.devices(device)[0] if device is not None else None
  define(
      "device_put",
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{device=}",
      lambda x: dispatch.device_put_p.bind(x, device=_device_fn(), src=None),
      [RandArg(shape, dtype)],
      shape=shape,
      dtype=dtype,
      device=device)
