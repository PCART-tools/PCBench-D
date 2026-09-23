def mean(a: ArrayLike, axis: Axis = None, dtype: DTypeLike | None = None,
         out: None = None, keepdims: bool = False, *,
         where: ArrayLike | None = None) -> Array:
  r"""Return the mean of array elements along a given axis.

  JAX implementation of :func:`numpy.mean`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      mean to be computed. If None, mean is computed along all the axes.
    dtype: The type of the output array. Default=None.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    where: optional, boolean array, default=None. The elements to be used in the
      mean. Array should be broadcast compatible to the input.
    out: Unused by JAX.

  Returns:
    An array of the mean along the given axis.

  See also:
    - :func:`jax.numpy.sum`: Compute the sum of array elements over a given axis.
    - :func:`jax.numpy.max`: Compute the maximum of array elements over given axis.
    - :func:`jax.numpy.min`: Compute the minimum of array elements over given axis.

  Examples:
    By default, the mean is computed along all the axes.

    >>> x = jnp.array([[1, 3, 4, 2],
    ...                [5, 2, 6, 3],
    ...                [8, 1, 2, 9]])
    >>> jnp.mean(x)
    Array(3.8333335, dtype=float32)

    If ``axis=1``, the mean is computed along axis 1.

    >>> jnp.mean(x, axis=1)
    Array([2.5, 4. , 5. ], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.mean(x, axis=1, keepdims=True)
    Array([[2.5],
           [4. ],
           [5. ]], dtype=float32)

    To use only specific elements of ``x`` to compute the mean, you can use
    ``where``.

    >>> where = jnp.array([[1, 0, 1, 0],
    ...                    [0, 1, 0, 1],
    ...                    [1, 1, 0, 1]], dtype=bool)
    >>> jnp.mean(x, axis=1, keepdims=True, where=where)
    Array([[2.5],
           [2.5],
           [6. ]], dtype=float32)
  """
  return _mean(a, _ensure_optional_axes(axis), dtype, out, keepdims,
               where=where)
