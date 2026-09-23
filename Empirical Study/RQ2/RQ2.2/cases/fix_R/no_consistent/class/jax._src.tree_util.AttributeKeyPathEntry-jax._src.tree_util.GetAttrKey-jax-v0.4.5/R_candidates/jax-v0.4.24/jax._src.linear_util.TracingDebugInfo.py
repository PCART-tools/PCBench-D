class TracingDebugInfo(NamedTuple):
  # Packages up trace/staging-time debug info about a func and its parameters,
  # formed just before staging to a jaxpr and read in trace-time error messages.
  # TODO(mattjj): delete partial_eval.DebugInfo, replace all uses with this cls
  traced_for: str             # e.g. 'jit', 'scan', etc
  func_src_info: str          # e.g. f'{fun.__name__} at {filename}:{lineno}'
  arg_names: tuple[str, ...]  # e.g. ('args[0]', ... )
  result_paths: Callable[[], tuple[str, ...]] | None
