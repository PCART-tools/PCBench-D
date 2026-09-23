def sum(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
        out: None = None, keepdims: bool = False, initial: ArrayLike | None = None,
        where: ArrayLike | None = None, promote_integers: bool = True) -> Array:
  r"""Sum of the elements of the array over a given axis.

  JAX implementation of :func:`numpy.sum`.

  Args:
    a: Input array.
    axis: int or array, default=None. Axis along which the sum to be computed.
      If None, the sum is computed along all the axes.
    dtype: The type of the output array. Default=None.
    out: Unused by JAX
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    initial: int or array, Default=None. Initial value for the sum.
    where: int or array, default=None. The elements to be used in the sum. Array
      should be broadcast compatible to the input.
    promote_integers : bool, default=True. If True, then integer inputs will be
      promoted to the widest available integer dtype, following numpy's behavior.
      If False, the result will have the same dtype as the input.
      ``promote_integers`` is ignored if ``dtype`` is specified.

  Returns:
    An array of the sum along the given axis.

  See also:
    - :func:`jax.numpy.prod`: Compute the product of array elements over a given
      axis.
    - :func:`jax.numpy.max`: Compute the maximum of array elements over given axis.
    - :func:`jax.numpy.min`: Compute the minimum of array elements over given axis.

  Examples:

    By default, the sum is computed along all the axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [5, 2, 6, 3],
    ...                [8, 1, 3, 9]])
    >>> jnp.sum(x)
    Array(47, dtype=int32)

    If ``axis=1``, the sum is computed along axis 1.

    >>> jnp.sum(x, axis=1)
    Array([10, 16, 21], dtype=int32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.sum(x, axis=1, keepdims=True)
    Array([[10],
           [16],
           [21]], dtype=int32)

    To include only specific elements in the sum, you can use ``where``.

    >>> where=jnp.array([[0, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.sum(x, axis=1, keepdims=True, where=where)
    Array([[ 4],
           [ 9],
           [12]], dtype=int32)
    >>> where=jnp.array([[False],
    ...                  [False],
    ...                  [False]])
    >>> jnp.sum(x, axis=0, keepdims=True, where=where)
    Array([[0, 0, 0, 0]], dtype=int32)
  """
  return _reduce_sum(a, axis=_ensure_optional_axes(axis), dtype=dtype, out=out,
                     keepdims=keepdims, initial=initial, where=where,
                     promote_integers=promote_integers)
