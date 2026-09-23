class JaxprDebugInfo(NamedTuple):
  traced_for: str     # e.g. 'jit', 'scan', etc
  func_src_info: str  # e.g. f'{fun.__name__} at {filename}:{lineno}'
  arg_names: tuple[str | None, ...]     # e.g. ('args[0]', ... )
  result_paths: tuple[str | None, ...]  # e.g. ('[0]', '[1]', ...)
