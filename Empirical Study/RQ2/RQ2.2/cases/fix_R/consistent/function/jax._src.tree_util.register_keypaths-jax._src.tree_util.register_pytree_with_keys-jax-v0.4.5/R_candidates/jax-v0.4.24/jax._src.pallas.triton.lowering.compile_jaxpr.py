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
  # TODO(sharadmv): handle multiple devices, right now we assume device 0
  # which is fine when we have multiple of the same GPU but this won't work in
  # general.
  device = 0
  arch = triton_kernel_call_lib.get_compute_capability(device)
  target = ("cuda", arch)
  cuda_backend = cb.CUDABackend(target)
  cuda_options = cuda_backend.parse_options(
      dict(
          num_warps=num_warps,
          num_stages=num_stages,
          debug=debug,
      )
  )
  lowering_result = lower_jaxpr_to_triton_module(
      jaxpr, in_shapes, grid_mapping, name, cuda_options
  )

  ttir = str(lowering_result.module)
  ptx, name, shared_mem_bytes, compute_capability, _ = (
      compile_ttir_to_ptx_inplace(
          lowering_result.module,
          cuda_backend,
          cuda_options,
          device=device,
      )
  )
  return TritonCompilationResult(
      name, ttir, ptx, shared_mem_bytes, compute_capability, lowering_result
  )
