def intersect1d(ar1: ArrayLike, ar2: ArrayLike, assume_unique: bool = False,
                return_indices: bool = False) -> Array | tuple[Array, Array, Array]:
  """Compute the set intersection of two 1D arrays.

  JAX implementation of :func:`numpy.intersect1d`.

  Because the size of the output of ``intersect1d`` is data-dependent, the function is not
  compatible with JIT or other JAX transformations.

  Args:
    ar1: first array of values to intersect.
    ar2: second array of values to intersect.
    assume_unique: if True, assume the input arrays contain unique values. This allows
      a more efficient implementation, but if ``assume_unique`` is True and the input
      arrays contain duplicates, the behavior is undefined. default: False.
    return_indices: If True, return arrays of indices specifying where the intersected
      values first appear in the input arrays.

  Returns:
    An array ``intersection``, or if ``return_indices=True``, a tuple of arrays
    ``(intersection, ar1_indices, ar2_indices)``. Returned values are

    - ``intersection``:
      A 1D array containing each value that appears in both ``ar1`` and ``ar2``.
    - ``ar1_indices``:
      *(returned if return_indices=True)* an array of shape ``intersection.shape`` containing
      the indices in flattened ``ar1`` of values in ``intersection``. For 1D inputs,
      ``intersection`` is equivalent to ``ar1[ar1_indices]``.
    - ``ar2_indices``:
      *(returned if return_indices=True)* an array of shape ``intersection.shape`` containing
      the indices in flattened ``ar2`` of values in ``intersection``. For 1D inputs,
      ``intersection`` is equivalent to ``ar2[ar2_indices]``.

  See also:
    - :func:`jax.numpy.union1d`: the set union of two 1D arrays.
    - :func:`jax.numpy.setxor1d`: the set XOR of two 1D arrays.
    - :func:`jax.numpy.setdiff1d`: the set difference of two 1D arrays.

  Examples:
    >>> ar1 = jnp.array([1, 2, 3, 4])
    >>> ar2 = jnp.array([3, 4, 5, 6])
    >>> jnp.intersect1d(ar1, ar2)
    Array([3, 4], dtype=int32)

    Computing intersection with indices:

    >>> intersection, ar1_indices, ar2_indices = jnp.intersect1d(ar1, ar2, return_indices=True)
    >>> intersection
    Array([3, 4], dtype=int32)

    ``ar1_indices`` gives the indices of the intersected values within ``ar1``:

     >>> ar1_indices
     Array([2, 3], dtype=int32)
     >>> jnp.all(intersection == ar1[ar1_indices])
     Array(True, dtype=bool)

    ``ar2_indices`` gives the indices of the intersected values within ``ar2``:

     >>> ar2_indices
     Array([0, 1], dtype=int32)
     >>> jnp.all(intersection == ar2[ar2_indices])
     Array(True, dtype=bool)
  """
  check_arraylike("intersect1d", ar1, ar2)
  ar1 = core.concrete_or_error(None, ar1, "The error arose in intersect1d()")
  ar2 = core.concrete_or_error(None, ar2, "The error arose in intersect1d()")

  if not assume_unique:
    if return_indices:
      ar1, ind1 = unique(ar1, return_index=True)
      ar2, ind2 = unique(ar2, return_index=True)
    else:
      ar1 = unique(ar1)
      ar2 = unique(ar2)
  else:
    ar1 = ravel(ar1)
    ar2 = ravel(ar2)

  if return_indices:
    aux, mask, aux_sort_indices = _intersect1d_sorted_mask(ar1, ar2, return_indices)
  else:
    aux, mask = _intersect1d_sorted_mask(ar1, ar2, return_indices)

  int1d = aux[:-1][mask]

  if return_indices:
    ar1_indices = aux_sort_indices[:-1][mask]
    ar2_indices = aux_sort_indices[1:][mask] - np.size(ar1)
    if not assume_unique:
      ar1_indices = ind1[ar1_indices]
      ar2_indices = ind2[ar2_indices]

    return int1d, ar1_indices, ar2_indices
  else:
    return int1d
