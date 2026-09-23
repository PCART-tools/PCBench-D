def _naryop_weak_type_rule(name, *avals, **kwargs):
  if any(aval.dtype == dtypes.float0 for aval in avals):
    pos = next(i for i, aval in enumerate(avals) if aval.dtype == dtypes.float0)
    raise TypeError(
        f"Called {name} with a float0 at position {pos}. "
        "float0s do not support any operations by design, because they "
        "are not compatible with non-trivial vector spaces. No implicit dtype "
        "conversion is done. You can use np.zeros_like(arr, dtype=np.float) "
        "to cast a float0 array to a regular zeros array. \n"
        "If you didn't expect to get a float0 you might have accidentally "
        "taken a gradient with respect to an integer argument.")
  return all(aval.weak_type for aval in avals)
