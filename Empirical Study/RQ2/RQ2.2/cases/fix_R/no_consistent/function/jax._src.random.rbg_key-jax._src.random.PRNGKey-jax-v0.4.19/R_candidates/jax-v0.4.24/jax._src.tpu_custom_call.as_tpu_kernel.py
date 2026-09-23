def as_tpu_kernel(
    module: ir.Module,
    out_type: Any,
    *,
    cost_estimate: CostEstimate | None = None,
    backend: str | xla_client.Client = "tpu",
    device_type: str | None = None,
    kernel_name: str | None = None,
    kernel_regeneration_metadata: bytes | None = None,
    vmem_limit_bytes: int | None = None,
    flags: dict[str, bool | int | float] | None = None,
    input_output_aliases: tuple[tuple[int, int], ...] = (),
) -> Callable[..., Any]:
  """Turns an MLIR Mosaic kernel into a JAX-compatible function."""
  # We use jax.jit to make sure we hit the fast compilation cache.
  some_tpu = jax.devices(backend)[0]
  device_kind = some_tpu.device_kind
  if not device_kind.startswith("TPU v"):
    raise ValueError(f"Unrecognized TPU device kind: {device_kind}.")
  if vmem_limit_bytes is not None and not isinstance(vmem_limit_bytes, int):
    raise ValueError(
        "vmem_limit_bytes must be an int: provided with a"
        f" {type(vmem_limit_bytes)}."
    )
  hardware_generation = int(device_kind[len("TPU v")])
  has_communication, has_custom_barrier = tpu.private_has_communication(
      module.operation
  )
  bytecode_buffer = io.BytesIO()
  module.operation.write_bytecode(bytecode_buffer, desired_version=0)
  asm = bytecode_buffer.getvalue()

  # TODO(amagni): Kernel name and regeneration metadata could alternatively be
  # added as a custom attribute to the MLIR call op rather than including them
  # in the backend_config.
  return _lowered_as_tpu_kernel(
      asm,
      out_type,
      needs_hlo_passes=_MOSAIC_ALLOW_HLO.value,
      needs_layout_passes=not device_type,
      device_type=device_type,
      has_communication=has_communication,
      has_custom_barrier=has_custom_barrier,
      kernel_name=kernel_name,
      kernel_regeneration_metadata=kernel_regeneration_metadata,
      cost_estimate=cost_estimate,
      vmem_limit_bytes=vmem_limit_bytes,
      flags=flags,
      input_output_aliases=input_output_aliases,
  )
