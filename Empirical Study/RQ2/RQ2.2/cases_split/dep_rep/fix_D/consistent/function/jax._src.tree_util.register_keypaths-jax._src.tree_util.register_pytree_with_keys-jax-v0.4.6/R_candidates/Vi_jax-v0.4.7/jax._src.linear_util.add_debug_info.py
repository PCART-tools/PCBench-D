def add_debug_info(f: WrappedFun, debug_info: Optional[TracingDebugInfo]
                   ) -> WrappedFun:
  """Produce a new WrappedFun with debug_info attached."""
  assert f.debug_info is None
  if debug_info is None:
    return f
  return WrappedFun(f.f, f.transforms, f.stores, f.params, f.in_type, debug_info)
