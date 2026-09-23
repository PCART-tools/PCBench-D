@partial(api.jit, static_argnames=('axis', 'keepdims'))
def nanmin(a: ArrayLike, axis: Axis = None, out: None = None,
           keepdims: bool = False, initial: ArrayLike | None = None,
           where: ArrayLike | None = None) -> Array:
  r"""Return the minimum of the array elements along a given axis, ignoring NaNs.

  JAX implementation of :func:`numpy.nanmin`.

  Args:
    a: Input array.
    axis: int or sequence of ints, default=None. Axis along which the minimum is
      computed. If None, the minimum is computed along the flattened array.
    keepdims: bool, default=False. If True, reduced axes are left in the result
      with size 1.
    initial: int or array, default=None. Initial value for the minimum.
    where: array of boolean dtype, default=None. The elements to be used in the
      minimum. Array should be broadcast compatible to the input. ``initial``
      must be specified when ``where`` is used.
    out: Unused by JAX.

  Returns:
    An array of minimum values along the given axis, ignoring NaNs. If all values
    are NaNs along the given axis, returns ``nan``.

  See also:
    - :func:`jax.numpy.nanmax`: Compute the maximum of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nansum`: Compute the sum of array elements along a given
      axis, ignoring NaNs.
    - :func:`jax.numpy.nanprod`: Compute the product of array elements along a
      given axis, ignoring NaNs.
    - :func:`jax.numpy.nanmean`: Compute the mean of array elements along a given
      axis, ignoring NaNs.

  Examples:

    By default, ``jnp.nanmin`` computes the minimum of elements along the flattened
    array.

    >>> nan = jnp.nan
    >>> x = jnp.array([[1, nan, 4, 5],
    ...                [nan, -2, nan, -4],
    ...                [2, 1, 3, nan]])
    >>> jnp.nanmin(x)
    Array(-4., dtype=float32)

    If ``axis=1``, the maximum will be computed along axis 1.

    >>> jnp.nanmin(x, axis=1)
    Array([ 1., -4.,  1.], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output will be same of that of the input.

    >>> jnp.nanmin(x, axis=1, keepdims=True)
    Array([[ 1.],
           [-4.],
           [ 1.]], dtype=float32)

    To include only specific elements in computing the maximum, you can use
    ``where``. It can either have same dimension as input

    >>> where=jnp.array([[0, 0, 1, 0],
    ...                  [0, 0, 1, 1],
    ...                  [1, 1, 1, 0]], dtype=bool)
    >>> jnp.nanmin(x, axis=1, keepdims=True, initial=0, where=where)
    Array([[ 0.],
           [-4.],
           [ 0.]], dtype=float32)

    or must be broadcast compatible with input.

    >>> where = jnp.array([[False],
    ...                    [True],
    ...                    [False]])
    >>> jnp.nanmin(x, axis=0, keepdims=True, initial=0, where=where)
    Array([[ 0., -2.,  0., -4.]], dtype=float32)
  """
  return _nan_reduction(a, 'nanmin', min, np.inf, nan_if_all_nan=initial is None,
                        axis=axis, out=out, keepdims=keepdims,
                        initial=initial, where=where)
