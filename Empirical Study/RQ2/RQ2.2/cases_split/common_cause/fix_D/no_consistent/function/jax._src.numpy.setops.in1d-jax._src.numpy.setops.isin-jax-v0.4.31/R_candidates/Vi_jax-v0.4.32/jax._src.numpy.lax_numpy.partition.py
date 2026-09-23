@partial(jit, static_argnames=['kth', 'axis'])
def partition(a: ArrayLike, kth: int, axis: int = -1) -> Array:
  """Returns a partially-sorted copy of an array.

  JAX implementation of :func:`numpy.partition`. The JAX version differs from
  NumPy in the treatment of NaN entries: NaNs which have the negative bit set
  are sorted to the beginning of the array.

  Args:
    a: array to be partitioned.
    kth: static integer index about which to partition the array.
    axis: static integer axis along which to partition the array; default is -1.

  Returns:
    A copy of ``a`` partitioned at the ``kth`` value along ``axis``. The entries
    before ``kth`` are values smaller than ``take(a, kth, axis)``, and entries
    after ``kth`` are indices of values larger than ``take(a, kth, axis)``

  Note:
    The JAX version requires the ``kth`` argument to be a static integer rather than
    a general array. This is implemented via two calls to :func:`jax.lax.top_k`. If
    you're only accessing the top or bottom k values of the output, it may be more
    efficient to call :func:`jax.lax.top_k` directly.

  See Also:
    - :func:`jax.numpy.sort`: full sort
    - :func:`jax.numpy.argpartition`: indirect partial sort
    - :func:`jax.lax.top_k`: directly find the top k entries
    - :func:`jax.lax.approx_max_k`: compute the approximate top k entries
    - :func:`jax.lax.approx_min_k`: compute the approximate bottom k entries

  Examples:
    >>> x = jnp.array([6, 8, 4, 3, 1, 9, 7, 5, 2, 3])
    >>> kth = 4
    >>> x_partitioned = jnp.partition(x, kth)
    >>> x_partitioned
    Array([1, 2, 3, 3, 4, 9, 8, 7, 6, 5], dtype=int32)

    The result is a partially-sorted copy of the input. All values before ``kth``
    are of smaller than the pivot value, and all values after ``kth`` are larger
    than the pivot value:

    >>> smallest_values = x_partitioned[:kth]
    >>> pivot_value = x_partitioned[kth]
    >>> largest_values = x_partitioned[kth + 1:]
    >>> print(smallest_values, pivot_value, largest_values)
    [1 2 3 3] 4 [9 8 7 6 5]

    Notice that among ``smallest_values`` and ``largest_values``, the returned
    order is arbitrary and implementation-dependent.
  """
  # TODO(jakevdp): handle NaN values like numpy.
  util.check_arraylike("partition", a)
  arr = asarray(a)
  if issubdtype(arr.dtype, np.complexfloating):
    raise NotImplementedError("jnp.partition for complex dtype is not implemented.")
  axis = _canonicalize_axis(axis, arr.ndim)
  kth = _canonicalize_axis(kth, arr.shape[axis])

  arr = swapaxes(arr, axis, -1)
  if dtypes.isdtype(arr.dtype, "unsigned integer"):
    # Here, we apply a trick to handle correctly 0 values for unsigned integers
    bottom = -lax.top_k(-(arr + 1), kth + 1)[0] - 1
  else:
    bottom = -lax.top_k(-arr, kth + 1)[0]
  top = lax.top_k(arr, arr.shape[-1] - kth - 1)[0]
  out = lax.concatenate([bottom, top], dimension=arr.ndim - 1)
  return swapaxes(out, -1, axis)
