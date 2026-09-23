def check_arg_avals_for_call(ref_avals, arg_avals):
  if len(ref_avals) != len(arg_avals):
    raise TypeError(
        f"Computation compiled for {len(ref_avals)} inputs "
        f"but called with {len(arg_avals)}")
  for ref_aval, arg_aval in zip(ref_avals, arg_avals):
    if not core.typematch(ref_aval, arg_aval):
      ref_avals_fmt = ', '.join(str(a) for a in ref_avals)
      arg_avals_fmt = ', '.join(str(a) for a in arg_avals)
      raise TypeError(
        f"Computation compiled for input types:\n  {ref_avals_fmt}\n"
        f"called with:\n  {arg_avals_fmt}")
