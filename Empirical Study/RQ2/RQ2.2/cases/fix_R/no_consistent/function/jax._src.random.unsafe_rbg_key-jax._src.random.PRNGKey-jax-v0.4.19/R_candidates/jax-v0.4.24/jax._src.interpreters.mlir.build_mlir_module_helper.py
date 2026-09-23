def build_mlir_module_helper(
    closed_jaxpr: core.ClosedJaxpr, *, name: str,
    platforms: Sequence[str],
    backend_or_name: str, axis_context: AxisContext) -> ir.Module:
  """Helper to generate pmap-style XLA computations for custom partitioners."""
  if closed_jaxpr.effects:
    raise NotImplementedError
  lowering_result = lower_jaxpr_to_module(name, closed_jaxpr,
      backend_or_name=backend_or_name, ordered_effects=[],
      name_stack=source_info_util.NameStack(),
      donated_args=[False] * len(closed_jaxpr.jaxpr.invars),
      axis_context=axis_context, platforms=platforms,
      lowering_parameters=LoweringParameters())
  return lowering_result.module
