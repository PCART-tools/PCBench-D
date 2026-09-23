def _lowered_as_tpu_kernel(
    lowered_module_asm: bytes,
    out_type: Any,
    constants: Sequence[Any] = (),
    *,
    device_type: str | None = None,
    has_communication: bool = False,
    has_custom_barrier: bool = False,
    kernel_name: str | None = None,
    kernel_regeneration_metadata: bytes | None = None,
):
  """Turns a low-level MLIR Mosaic kernel into a JAX-compatible function."""
  unpack = False
  if not isinstance(out_type, collections.abc.Iterable):
    out_type = (out_type,)
    unpack = True
  out_avals = tuple(core.ShapedArray(ty.shape, ty.dtype) for ty in out_type)
  def apply_kernel(*args, collective_id: int | None = None):
    if has_custom_barrier:
      if collective_id is None:
        raise ValueError(
            "collective_id has to be specified when using a custom barrier"
        )
    elif collective_id is not None:
      raise ValueError(
          "collective_id has to be unspecified or None when not using a custom"
          " barrier"
      )
    config = CustomCallBackendConfig(
        lowered_module_asm,
        has_communication,
        collective_id,
        device_type,
        kernel_name,
        kernel_regeneration_metadata,
    )
    result = tpu_custom_call_p.bind(
        *args,
        *constants,
        config=config,
        out_avals=out_avals,
    )
    return result[0] if unpack else result
  return jax.jit(apply_kernel, static_argnames=["collective_id"])
