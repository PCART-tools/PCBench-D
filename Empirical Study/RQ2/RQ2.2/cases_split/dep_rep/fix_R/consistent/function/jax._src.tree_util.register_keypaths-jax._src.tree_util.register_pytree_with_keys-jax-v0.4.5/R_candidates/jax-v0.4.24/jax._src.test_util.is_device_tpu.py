def is_device_tpu(version: int | None = None, variant: str = "") -> bool:
  if device_under_test() != "tpu":
    return False
  if version is None:
    return True
  device_kind = jax.devices()[0].device_kind
  expected_version = f"v{version}{variant}"
  # Special case v5e until the name is updated in device_kind
  if expected_version == "v5e":
    return "v5 lite" in device_kind
  return expected_version in device_kind
