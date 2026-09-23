def isin(element: ArrayLike, test_elements: ArrayLike,
         assume_unique: bool = False, invert: bool = False, *,
         method='auto') -> Array:
  """Determine whether elements in ``element`` appear in ``test_elements``.

  JAX implementation of :func:`numpy.isin`.

  Args:
    element: input array of elements for which membership will be checked.
    test_elements: N-dimensional array of test values to check for the presence of
      each element.
    invert: If True, return ``~isin(element, test_elements)``. Default is False.
    assume_unique: if true, input arrays are assumed to be unique, which can
      lead to more efficient computation. If the input arrays are not unique
      and assume_unique is set to True, the results are undefined.
    method: string specifying the method used to compute the result. Supported
      options are 'compare_all', 'binary_search', 'sort', and 'auto' (default).

  Returns:
    A boolean array of shape ``element.shape`` that specifies whether each element
    appears in ``test_elements``.

  Examples:
    >>> elements = jnp.array([1, 2, 3, 4])
    >>> test_elements = jnp.array([[1, 5, 6, 3, 7, 1]])
    >>> jnp.isin(elements, test_elements)
    Array([ True, False,  True, False], dtype=bool)
  """
  check_arraylike("isin", element, test_elements)
  result = _in1d(element, test_elements, invert=invert,
                 method=method, assume_unique=assume_unique)
  return result.reshape(np.shape(element))
