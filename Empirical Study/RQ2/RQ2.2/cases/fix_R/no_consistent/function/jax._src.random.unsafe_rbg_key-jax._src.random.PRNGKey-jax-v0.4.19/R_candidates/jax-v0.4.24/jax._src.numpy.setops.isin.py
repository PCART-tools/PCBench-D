@implements(np.isin, lax_description="""
In the JAX version, the `assume_unique` argument is not referenced.
""")
def isin(element: ArrayLike, test_elements: ArrayLike,
         assume_unique: bool = False, invert: bool = False) -> Array:
  del assume_unique  # unused
  check_arraylike("isin", element, test_elements)
  result = _in1d(element, test_elements, invert=invert)
  return result.reshape(np.shape(element))
