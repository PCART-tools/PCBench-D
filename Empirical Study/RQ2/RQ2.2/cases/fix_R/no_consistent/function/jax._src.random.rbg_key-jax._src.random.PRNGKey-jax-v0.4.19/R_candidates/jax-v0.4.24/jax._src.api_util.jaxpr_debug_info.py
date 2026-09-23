def jaxpr_debug_info(jaxpr: core.Jaxpr, trace_debug: TracingDebugInfo | None,
                     result_paths: tuple[str | None, ...] | None = None,
                     ) -> core.Jaxpr:
  """Add debug info to jaxpr, given trace-time debug info and result paths."""
  if trace_debug is None:
    return jaxpr
  assert (result_paths is not None) ^ (trace_debug.result_paths is not None)
  if result_paths is None:
    result_paths = trace_debug.result_paths()  # type: ignore
  debug_info = core.JaxprDebugInfo(
      trace_debug.traced_for, trace_debug.func_src_info,
      trace_debug.arg_names, tuple(result_paths))
  return jaxpr.replace(debug_info=debug_info)
