@_wraps(np.isin, lax_description="""
In the JAX version, the `assume_unique` argument is not referenced.
""")
def isin(element: ArrayLike, test_elements: ArrayLike,
         assume_unique: bool = False, invert: bool = False) -> Array:
  result = in1d(element, test_elements, assume_unique=assume_unique, invert=invert)
  return result.reshape(np.shape(element))
