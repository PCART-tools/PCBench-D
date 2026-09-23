def check_arg_avals_for_call(ref_avals, arg_avals,
                             jaxpr_debug_info: core.JaxprDebugInfo | None = None):
  if len(ref_avals) != len(arg_avals):
    raise TypeError(
        f"Computation compiled for {len(ref_avals)} inputs "
        f"but called with {len(arg_avals)}")

  if jaxpr_debug_info is not None:
    arg_names = [f"'{name}'" for name in jaxpr_debug_info.arg_names]
  else:
    num_args = len(ref_avals)
    arg_names = [f"{i + 1}/{num_args}" for i in range(num_args)]

  errors = []
  for ref_aval, arg_aval, name in safe_zip(ref_avals, arg_avals, arg_names):
    if not core.typematch(ref_aval, arg_aval):
      errors.append(
          f"Argument {name} compiled with {ref_aval.str_short()} and called "
          f"with {arg_aval.str_short()}")
  if errors:
    max_num_errors = 5
    str_errors = "\n".join(errors[:max_num_errors])
    if len(errors) >= max_num_errors:
      num_mismatch_str = f"The first {max_num_errors} of {len(errors)}"
    else:
      num_mismatch_str = "The"
    raise TypeError(
        "Argument types differ from the types for which this computation was "
        f"compiled. {num_mismatch_str} mismatches are:\n{str_errors}")
