def as_tpu_kernel(
    module: ir.Module,
    out_type: Any,
    *,
    backend: str | xla_client.Client = "tpu",
    device_type: str | None = None,
    kernel_name: str | None = None,
    kernel_regeneration_metadata: bytes | None = None,
) -> Callable[..., Any]:
  """Turns an MLIR Mosaic kernel into a JAX-compatible function."""
  # We use jax.jit to make sure we hit the fast compilation cache.
  some_tpu = jax.devices(backend)[0]
  device_kind = some_tpu.device_kind
  if device_kind.endswith(" pod"):
    device_kind = device_kind[:-len(" pod")]
  if device_kind.endswith(" lite"):
    device_kind = device_kind[:-len(" lite")]
  assert device_kind[:-1] == "TPU v", device_kind
  hardware_generation = int(device_kind[-1])
  has_communication, has_custom_barrier = tpu.private_has_communication(
      module.operation
  )
  lowered_module_asm, constants = _lower_tpu_kernel(
      module, hardware_generation, device_type=device_type
  )
  # TODO(amagni): Kernel name and regeneration metadata could alternatively be
  # added as a custom attribute to the MLIR call op rather than including them
  # in the backend_config.
  return _lowered_as_tpu_kernel(
      lowered_module_asm,
      out_type,
      constants,
      device_type=device_type,
      has_communication=has_communication,
      has_custom_barrier=has_custom_barrier,
      kernel_name=kernel_name,
      kernel_regeneration_metadata=kernel_regeneration_metadata,
  )
