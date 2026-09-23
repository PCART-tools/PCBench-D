def get_tpu_version() -> int:
  if device_under_test() != "tpu":
    raise ValueError("Device is not TPU")
  kind = jax.devices()[0].device_kind
  if kind.endswith(' lite'):
    kind = kind[:-len(' lite')]
  assert kind[:-1] == "TPU v", kind
  return int(kind[-1])
