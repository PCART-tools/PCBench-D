@weakref_lru_cache
def compile_jaxpr(
    jaxpr: jax_core.Jaxpr,
    in_shapes,
    grid_mapping: GridMapping,
    name: str,
    num_warps: int,
    num_stages: int,
    debug: bool,
) -> TritonCompilationResult:
  lowering_result = lower_jaxpr_to_triton_module(
      jaxpr, in_shapes, grid_mapping, name
  )
  device = 0
  ttir = str(lowering_result.module)
  ptx, name, shared_mem_bytes, compute_capability = compile_ttir_to_ptx_inplace(
      lowering_result.module,
      device=device,
      num_warps=num_warps,
      num_stages=num_stages,
      dump=debug,
  )
  return TritonCompilationResult(
      name, ttir, ptx, shared_mem_bytes, compute_capability, lowering_result
  )
