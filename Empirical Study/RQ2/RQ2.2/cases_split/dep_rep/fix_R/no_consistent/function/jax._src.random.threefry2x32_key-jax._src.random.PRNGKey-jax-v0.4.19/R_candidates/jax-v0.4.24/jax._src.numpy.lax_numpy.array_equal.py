@util.implements(np.array_equal)
def array_equal(a1: ArrayLike, a2: ArrayLike, equal_nan: bool = False) -> Array:
  try:
    a1, a2 = asarray(a1), asarray(a2)
  except Exception as err:
    # TODO(jakevdp): Deprecated 2023-11-23; change to error.
    warnings.warn("Inputs to array_equal() cannot be coerced to array. "
                  "Returning False; in the future this will raise an exception.\n"
                  f"{err!r}",
                  DeprecationWarning, stacklevel=2)
    return bool_(False)
  if shape(a1) != shape(a2):
    return bool_(False)
  eq = asarray(a1 == a2)
  if equal_nan:
    eq = ufuncs.logical_or(eq, ufuncs.logical_and(ufuncs.isnan(a1), ufuncs.isnan(a2)))
  return reductions.all(eq)
