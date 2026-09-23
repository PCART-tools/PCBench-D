def setxor1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False, *,
             size: int | None = None, fill_value: ArrayLike | None = None) -> Array:
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
    size: if specified, return only the first ``size`` sorted elements. If there are fewer
      elements than ``size`` indicates, the return value will be padded with ``fill_value``,
      and returned indices will be padded with an out-of-bound index.
    fill_value: when ``size`` is specified and there are fewer than the indicated number of
      elements, fill the remaining entries ``fill_value``. Defaults to the smallest value
      in the xor result.

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
  arr1, arr2 = promote_dtypes(ravel(ar1), ravel(ar2))
  del ar1, ar2

  if size is not None:
    return _setxor1d_size(arr1, arr2, fill_value=fill_value,
                          assume_unique=assume_unique, size=size)

  if not assume_unique:
    arr1 = unique(arr1)
    arr2 = unique(arr2)
  aux = concatenate((arr1, arr2))
  if aux.size == 0:
    return aux
  aux = sort(aux)
  flag = concatenate((True, aux[1:] != aux[:-1], True), axis=None)
  return aux[flag[1:] & flag[:-1]]
