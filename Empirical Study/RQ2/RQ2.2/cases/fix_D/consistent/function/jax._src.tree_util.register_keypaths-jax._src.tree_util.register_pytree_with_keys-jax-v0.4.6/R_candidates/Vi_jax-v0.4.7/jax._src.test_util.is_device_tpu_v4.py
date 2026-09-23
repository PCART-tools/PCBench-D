def is_device_tpu_v4():
  return jax.devices()[0].device_kind == "TPU v4"
