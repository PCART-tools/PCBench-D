def make_ir_context() -> ir.Context:
  """Creates an MLIR context suitable for JAX IR."""
  from jax._src.lib.mlir import dialects
  context = ir.Context()
  dialects.mhlo.register_mhlo_dialect(context)
  dialects.chlo.register_dialect(context)
  dialects.stablehlo.register_dialect(context)
  return context
