def jaxpr_debug_info(jaxpr: core.Jaxpr, trace_debug: Optional[TracingDebugInfo],
                     result_paths: Optional[Tuple[Optional[str], ...]] = None,
                     ) -> core.Jaxpr:
  """Add debug info to jaxpr, given trace-time debug info and result paths."""
  if trace_debug is None:
    return jaxpr
  assert (result_paths is not None) ^ (trace_debug.result_paths is not None)
  if result_paths is None:
    result_paths = trace_debug.result_paths()  # type: ignore
  debug_info = core.JaxprDebugInfo(
      trace_debug.traced_for, trace_debug.func_src_info,
      trace_debug.arg_names, result_paths)
  return jaxpr.replace(debug_info=debug_info)
