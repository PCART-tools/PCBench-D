def isin(element: ArrayLike, test_elements: ArrayLike,
         assume_unique: bool = False, invert: bool = False) -> Array:
  """Determine whether elements in ``element`` appear in ``test_elements``.

  JAX implementation of :func:`numpy.isin`.

  Args:
    element: input array of elements for which membership will be checked.
    test_elements: N-dimensional array of test values to check for the presence of
      each element.
    invert: If True, return ``~isin(element, test_elements)``. Default is False.
    assume_unique: unused by JAX

  Returns:
    A boolean array of shape ``element.shape`` that specifies whether each element
    appears in ``test_elements``.

  Examples:
    >>> elements = jnp.array([1, 2, 3, 4])
    >>> test_elements = jnp.array([[1, 5, 6, 3, 7, 1]])
    >>> jnp.isin(elements, test_elements)
    Array([ True, False,  True, False], dtype=bool)
  """
  del assume_unique  # unused
  check_arraylike("isin", element, test_elements)
  result = _in1d(element, test_elements, invert=invert)
  return result.reshape(np.shape(element))
