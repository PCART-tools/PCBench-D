def _promote_weak_typed_inputs(in_vals, in_avals, out_avals):
  """Promote weakly-typed in_vals to be compatible with out_avals.

  Args:
    in_vals : flattened list of input values.
    in_avals : corresponding list of avals.
    out_avals : list of target output avals.
  Returns:
    in_vals_new : flattened list of modified in_vals with no weak types.
    changed : bool; true if in_vals required modification.
  """
  if len(in_vals) != len(in_avals) or len(in_avals) != len(out_avals):
    # Calling function is responsible for catching this.
    return in_vals, False
  weak_mismatches = [i for i, (a1, a2) in enumerate(zip(in_avals, out_avals))
                    if getattr(a1, 'weak_type', False) and not core.typematch(a1, a2)]
  if not weak_mismatches:
    return in_vals, False
  for i in weak_mismatches:
    new_dtype = dtypes.result_type(in_vals[i], out_avals[i])
    in_vals[i] = lax.convert_element_type(in_vals[i], new_dtype)
  return in_vals, True
