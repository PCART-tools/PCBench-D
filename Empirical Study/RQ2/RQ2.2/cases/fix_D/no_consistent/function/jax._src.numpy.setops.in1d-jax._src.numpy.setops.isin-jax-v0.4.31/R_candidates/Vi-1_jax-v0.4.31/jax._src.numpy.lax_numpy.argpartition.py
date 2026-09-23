@partial(jit, static_argnames=['kth', 'axis'])
def argpartition(a: ArrayLike, kth: int, axis: int = -1) -> Array:
  """Returns indices that partially sort an array.

  JAX implementation of :func:`numpy.argpartition`. The JAX version differs from
  NumPy in the treatment of NaN entries: NaNs which have the negative bit set are
  sorted to the beginning of the array.

  Args:
    a: array to be partitioned.
    kth: static integer index about which to partition the array.
    axis: static integer axis along which to partition the array; default is -1.

  Returns:
    Indices which partition ``a`` at the ``kth`` value along ``axis``. The entries
    before ``kth`` are indices of values smaller than ``take(a, kth, axis)``, and
    entries after ``kth`` are indices of values larger than ``take(a, kth, axis)``

  Note:
    The JAX version requires the ``kth`` argument to be a static integer rather than
    a general array. This is implemented via two calls to :func:`jax.lax.top_k`. If
    you're only accessing the top or bottom k values of the output, it may be more
    efficient to call :func:`jax.lax.top_k` directly.

  See Also:
    - :func:`jax.numpy.partition`: direct partial sort
    - :func:`jax.numpy.argsort`: full indirect sort
    - :func:`jax.lax.top_k`: directly find the top k entries
    - :func:`jax.lax.approx_max_k`: compute the approximate top k entries
    - :func:`jax.lax.approx_min_k`: compute the approximate bottom k entries

  Examples:
    >>> x = jnp.array([6, 8, 4, 3, 1, 9, 7, 5, 2, 3])
    >>> kth = 4
    >>> idx = jnp.argpartition(x, kth)
    >>> idx
    Array([4, 8, 3, 9, 2, 0, 1, 5, 6, 7], dtype=int32)

    The result is a sequence of indices that partially sort the input. All indices
    before ``kth`` are of values smaller than the pivot value, and all indices
    after ``kth`` are of values larger than the pivot value:

    >>> x_partitioned = x[idx]
    >>> smallest_values = x_partitioned[:kth]
    >>> pivot_value = x_partitioned[kth]
    >>> largest_values = x_partitioned[kth + 1:]
    >>> print(smallest_values, pivot_value, largest_values)
    [1 2 3 3] 4 [6 8 9 7 5]

    Notice that among ``smallest_values`` and ``largest_values``, the returned
    order is arbitrary and implementation-dependent.
  """
  # TODO(jakevdp): handle NaN values like numpy.
  util.check_arraylike("partition", a)
  arr = asarray(a)
  if issubdtype(arr.dtype, np.complexfloating):
    raise NotImplementedError("jnp.argpartition for complex dtype is not implemented.")
  axis = _canonicalize_axis(axis, arr.ndim)
  kth = _canonicalize_axis(kth, arr.shape[axis])

  arr = swapaxes(arr, axis, -1)
  if dtypes.isdtype(arr.dtype, "unsigned integer"):
    # Here, we apply a trick to handle correctly 0 values for unsigned integers
    bottom_ind = lax.top_k(-(arr + 1), kth + 1)[1]
  else:
    bottom_ind = lax.top_k(-arr, kth + 1)[1]

  # To avoid issues with duplicate values, we compute the top indices via a proxy
  set_to_zero = lambda a, i: a.at[i].set(0)
  for _ in range(arr.ndim - 1):
    set_to_zero = jax.vmap(set_to_zero)
  proxy = set_to_zero(ones(arr.shape), bottom_ind)
  top_ind = lax.top_k(proxy, arr.shape[-1] - kth - 1)[1]
  out = lax.concatenate([bottom_ind, top_ind], dimension=arr.ndim - 1)
  return swapaxes(out, -1, axis)
