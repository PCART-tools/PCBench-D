def std(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
        out: None = None, ddof: int = 0, keepdims: bool = False, *,
        where: ArrayLike | None = None, correction: int | float | None = None) -> Array:
  r"""Compute the standard deviation along a given axis.

  JAX implementation of :func:`numpy.std`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      standard deviation is computed. If None, standard deviaiton is computed
      along all the axes.
    dtype: The type of the output array. Default=None.
    ddof: int, default=0. Degrees of freedom. The divisor in the standard deviation
      computation is ``N-ddof``, ``N`` is number of elements along given axis.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      standard deviation. Array should be broadcast compatible to the input.
    correction: int or float, default=None. Alternative name for ``ddof``.
      Both ddof and correction can't be provided simultaneously.
    out: Unused by JAX.

  Returns:
    An array of the standard deviation along the given axis.

  See also:
    - :func:`jax.numpy.var`: Compute the variance of array elements over given
      axis.
    - :func:`jax.numpy.mean`: Compute the mean of array elements over a given axis.
    - :func:`jax.numpy.nanvar`: Compute the variance along a given axis, ignoring
      NaNs values.
    - :func:`jax.numpy.nanstd`: Computed the standard deviation of a given axis,
      ignoring NaN values.

  Examples:
    By default, ``jnp.std`` computes the standard deviation along all axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [4, 2, 5, 3],
    ...                [5, 4, 2, 3]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.std(x)
    Array(1.21, dtype=float32)

    If ``axis=0``, computes along axis 0.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.std(x, axis=0))
    [1.7  0.82 1.25 0.47]

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.std(x, axis=0, keepdims=True))
    [[1.7  0.82 1.25 0.47]]

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.std(x, axis=0, keepdims=True, ddof=1))
    [[2.08 1.   1.53 0.58]]

    To include specific elements of the array to compute standard deviation, you
    can use ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 0, 1],
    ...                    [1, 1, 1, 0]], dtype=bool)
    >>> jnp.std(x, axis=0, keepdims=True, where=where)
    Array([[2., 1., 1., 0.]], dtype=float32)
  """
  if correction is None:
    correction = ddof
  elif not isinstance(ddof, int) or ddof != 0:
    raise ValueError("ddof and correction can't be provided simultaneously.")
  return _std(a, _ensure_optional_axes(axis), dtype, out, correction, keepdims,
              where=where)
