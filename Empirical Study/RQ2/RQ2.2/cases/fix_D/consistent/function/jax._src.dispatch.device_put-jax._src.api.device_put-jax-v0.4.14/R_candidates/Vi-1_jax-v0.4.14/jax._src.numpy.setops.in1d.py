@_wraps(np.in1d, lax_description="""
In the JAX version, the `assume_unique` argument is not referenced.
""")
def in1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False, invert: bool = False) -> Array:
  del assume_unique  # unused
  return _in1d(ar1, ar2, invert)
