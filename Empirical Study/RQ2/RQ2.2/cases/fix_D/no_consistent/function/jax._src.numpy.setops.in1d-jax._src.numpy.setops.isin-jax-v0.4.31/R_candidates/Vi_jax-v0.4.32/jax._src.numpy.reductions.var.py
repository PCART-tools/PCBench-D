def var(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
        out: None = None, ddof: int = 0, keepdims: bool = False, *,
        where: ArrayLike | None = None, correction: int | float | None = None) -> Array:
  r"""Compute the variance along a given axis.

  JAX implementation of :func:`numpy.var`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      variance is computed. If None, variance is computed along all the axes.
    dtype: The type of the output array. Default=None.
    ddof: int, default=0. Degrees of freedom. The divisor in the variance computation
      is ``N-ddof``, ``N`` is number of elements along given axis.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      variance. Array should be broadcast compatible to the input.
    correction: int or float, default=None. Alternative name for ``ddof``.
      Both ddof and correction can't be provided simultaneously.
    out: Unused by JAX.

  Returns:
    An array of the variance along the given axis.

  See also:
    - :func:`jax.numpy.mean`: Compute the mean of array elements over a given axis.
    - :func:`jax.numpy.std`: Compute the standard deviation of array elements over
      given axis.
    - :func:`jax.numpy.nanvar`: Compute the variance along a given axis, ignoring
      NaNs values.
    - :func:`jax.numpy.nanstd`: Computed the standard deviation of a given axis,
      ignoring NaN values.

  Examples:
    By default, ``jnp.var`` computes the variance along all axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [5, 2, 6, 3],
    ...                [8, 4, 2, 9]])
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   jnp.var(x)
    Array(5.74, dtype=float32)

    If ``axis=1``, variance is computed along axis 1.

    >>> jnp.var(x, axis=1)
    Array([1.25  , 2.5   , 8.1875], dtype=float32)

    To preserve the dimensions of input, you can set ``keepdims=True``.

    >>> jnp.var(x, axis=1, keepdims=True)
    Array([[1.25  ],
           [2.5   ],
           [8.1875]], dtype=float32)

    If ``ddof=1``:

    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.var(x, axis=1, keepdims=True, ddof=1))
    [[ 1.67]
     [ 3.33]
     [10.92]]

    To include specific elements of the array to compute variance, you can use
    ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 1, 0],
    ...                    [1, 1, 1, 0]], dtype=bool)
    >>> with jnp.printoptions(precision=2, suppress=True):
    ...   print(jnp.var(x, axis=1, keepdims=True, where=where))
    [[2.25]
     [4.  ]
     [6.22]]
  """
  if correction is None:
    correction = ddof
  elif not isinstance(ddof, int) or ddof != 0:
    raise ValueError("ddof and correction can't be provided simultaneously.")
  return _var(a, _ensure_optional_axes(axis), dtype, out, correction, keepdims,
              where=where)
