def typecompat(aval_ref: AbstractValue, aval: AbstractValue) -> bool:
  """Determine whether `aval` conforms to `aval_ref`.

  Ignores weak_type and named_shape, other than to check that an axis name isn't
  used with different sizes.
  """
  try:
    return typematch(aval_ref, lattice_join(aval_ref, aval))
  except TypeError:
    return False
