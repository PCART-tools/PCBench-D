def check_arg_avals_for_call(ref_avals, arg_avals):
  if len(ref_avals) != len(arg_avals):
    raise TypeError(
        f"Computation compiled for {len(ref_avals)} inputs "
        f"but called with {len(arg_avals)}")
  for ref_aval, arg_aval in zip(ref_avals, arg_avals):
    if not core.typematch(ref_aval, arg_aval):
      raise TypeError(
        "Computation was compiled for different input types and called with "
        "different types. One of the mismatches is:\n"
        f"Compiled with:\n {ref_aval}\n"
        f"called with:\n {arg_aval}")
