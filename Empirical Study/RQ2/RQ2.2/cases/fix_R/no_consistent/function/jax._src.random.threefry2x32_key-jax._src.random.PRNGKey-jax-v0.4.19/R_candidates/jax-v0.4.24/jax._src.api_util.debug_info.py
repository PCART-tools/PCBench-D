def debug_info(traced_for: str, fun: Callable, args: tuple[Any],
               kwargs: dict[str, Any], static_argnums: tuple[int, ...],
               static_argnames: tuple[str, ...]) -> TracingDebugInfo | None:
  """Try to build trace-time debug info for fun when applied to args/kwargs."""
  src = fun_sourceinfo(fun)
  arg_names = _arg_names(fun, args, kwargs, static_argnums, static_argnames)
  if src is None or arg_names is None:
    return None
  return TracingDebugInfo(traced_for, src, arg_names, None)
