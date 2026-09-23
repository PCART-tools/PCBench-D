@_wraps(np.setxor1d, lax_description="""
In the JAX version, the input arrays are explicitly flattened regardless
of assume_unique value.
""")
def setxor1d(ar1, ar2, assume_unique=False):
  _check_arraylike("setxor1d", ar1, ar2)
  ar1 = core.concrete_or_error(None, ar1, "The error arose in setxor1d()")
  ar2 = core.concrete_or_error(None, ar2, "The error arose in setxor1d()")

  ar1 = ravel(ar1)
  ar2 = ravel(ar2)

  if not assume_unique:
    ar1 = unique(ar1)
    ar2 = unique(ar2)

  aux = concatenate((ar1, ar2))
  if aux.size == 0:
    return aux

  aux = sort(aux)
  flag = concatenate((array([True]), aux[1:] != aux[:-1], array([True])))
  return aux[flag[1:] & flag[:-1]]
