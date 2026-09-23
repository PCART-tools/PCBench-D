def build_xla_computation_helper(
    closed_jaxpr: core.ClosedJaxpr, *, name: str, platform: str,
    backend_or_name: str, axis_context: AxisContext) -> xc.XlaComputation:
  """Helper to generate pmap-style XLA computations for custom partitioners."""
  if closed_jaxpr.effects:
    raise NotImplementedError
  lowering_result = lower_jaxpr_to_module(name, closed_jaxpr,
      backend_or_name=backend_or_name, unordered_effects=[], ordered_effects=[],
      name_stack=source_info_util.NameStack(),
      donated_args=[False] * len(closed_jaxpr.jaxpr.invars),
      axis_context=axis_context, platform=platform)
  return xc._xla.mlir.mlir_module_to_xla_computation(
      module_to_string(lowering_result.module), use_tuple_args=False,
      return_tuple=False)
