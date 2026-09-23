def setxor1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False) -> Array:
  """Compute the set-wise xor of elements in two arrays.

  JAX implementation of :func:`numpy.setxor1d`.

  Because the size of the output of ``setxor1d`` is data-dependent, the function is not
  compatible with JIT or other JAX transformations.

  Args:
    ar1: first array of values to intersect.
    ar2: second array of values to intersect.
    assume_unique: if True, assume the input arrays contain unique values. This allows
      a more efficient implementation, but if ``assume_unique`` is True and the input
      arrays contain duplicates, the behavior is undefined. default: False.

  Returns:
    An array of values that are found in exactly one of the input arrays.

  See also:
    - :func:`jax.numpy.intersect1d`: the set intersection of two 1D arrays.
    - :func:`jax.numpy.union1d`: the set union of two 1D arrays.
    - :func:`jax.numpy.setdiff1d`: the set difference of two 1D arrays.

  Examples:
    >>> ar1 = jnp.array([1, 2, 3, 4])
    >>> ar2 = jnp.array([3, 4, 5, 6])
    >>> jnp.setxor1d(ar1, ar2)
    Array([1, 2, 5, 6], dtype=int32)
  """
  check_arraylike("setxor1d", ar1, ar2)
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
