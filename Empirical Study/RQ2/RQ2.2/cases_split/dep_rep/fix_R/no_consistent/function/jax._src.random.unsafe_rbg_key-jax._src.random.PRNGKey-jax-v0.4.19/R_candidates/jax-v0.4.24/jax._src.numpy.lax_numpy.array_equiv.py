@util.implements(np.array_equiv)
def array_equiv(a1: ArrayLike, a2: ArrayLike) -> Array:
  try:
    a1, a2 = asarray(a1), asarray(a2)
  except Exception as err:
    # TODO(jakevdp): Deprecated 2023-11-23; change to error.
    warnings.warn("Inputs to array_equiv() cannot be coerced to array. "
                  "Returning False; in the future this will raise an exception.\n"
                  f"{err!r}",
                  DeprecationWarning, stacklevel=2)
    return bool_(False)
  try:
    eq = ufuncs.equal(a1, a2)
  except ValueError:
    # shapes are not broadcastable
    return bool_(False)
  return reductions.all(eq)
