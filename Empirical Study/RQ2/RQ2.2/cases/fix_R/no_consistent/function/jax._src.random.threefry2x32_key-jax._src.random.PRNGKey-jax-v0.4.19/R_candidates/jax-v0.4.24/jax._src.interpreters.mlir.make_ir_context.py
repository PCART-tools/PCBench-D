def make_ir_context() -> ir.Context:
  """Creates an MLIR context suitable for JAX IR."""
  context = ir.Context()
  context.append_dialect_registry(upstream_dialects)
  context.load_all_available_dialects()

  # If threading is enabled, each MLIR context will keep alive a thread pool.
  # Since we cache MLIR modules (and hence contexts), this means we might keep
  # several threads alive for each cache entry. This is a terrible idea. However
  # we don't do any heavy computation on MLIR modules from Python anyway, so we
  # just disable threading.
  context.enable_multithreading(False)

  dialects.mhlo.register_mhlo_dialect(context)
  dialects.chlo.register_dialect(context)
  dialects.hlo.register_dialect(context)
  return context
