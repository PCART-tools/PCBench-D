def _maybe_device_put(arr: Array, device: xc.Device | Sharding | None) -> Array:
  return arr if device is None else jax.device_put(arr, device)
