@_wraps(np.isin, lax_description="""
In the JAX version, the `assume_unique` argument is not referenced.
""")
def isin(element, test_elements, assume_unique=False, invert=False):  # noqa: F811
  result = in1d(element, test_elements, assume_unique=assume_unique, invert=invert)
  return result.reshape(np.shape(element))
