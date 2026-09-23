def annotate(f: WrappedFun, in_type: core.InputType) -> WrappedFun:
  assert f.in_type is None
  if in_type is None:
    return f
  _check_input_type(in_type)
  return WrappedFun(f.f, f.transforms, f.stores, f.params, in_type)
