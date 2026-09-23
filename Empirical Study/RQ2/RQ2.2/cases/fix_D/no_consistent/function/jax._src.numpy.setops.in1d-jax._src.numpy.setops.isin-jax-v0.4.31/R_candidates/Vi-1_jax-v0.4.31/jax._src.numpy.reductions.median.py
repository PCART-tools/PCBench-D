@partial(api.jit, static_argnames=('axis', 'overwrite_input', 'keepdims'))
def median(a: ArrayLike, axis: int | tuple[int, ...] | None = None,
           out: None = None, overwrite_input: bool = False,
           keepdims: bool = False) -> Array:
  r"""Return the median of array elements along a given axis.

  JAX implementation of :func:`numpy.median`.

  Args:
    a: input array.
    axis: optional, int or sequence of ints, default=None. Axis along which the
      median to be computed. If None, median is computed for the flattened array.
    keepdims: bool, default=False. If true, reduced axes are left in the result
      with size 1.
    out: Unused by JAX.
    overwrite_input: Unused by JAX.

  Returns:
    An array of the median along the given axis.

  See also:
    - :func:`jax.numpy.mean`: Compute the mean of array elements over a given axis.
    - :func:`jax.numpy.max`: Compute the maximum of array elements over given axis.
    - :func:`jax.numpy.min`: Compute the minimum of array elements over given axis.

  Examples:
    By default, the median is computed for the flattened array.

    >>> x = jnp.array([[2, 4, 7, 1],
    ...                [3, 5, 9, 2],
    ...                [6, 1, 8, 3]])
    >>> jnp.median(x)
    Array(3.5, dtype=float32)

    If ``axis=1``, the median is computed along axis 1.

    >>> jnp.median(x, axis=1)
    Array([3. , 4. , 4.5], dtype=float32)

    If ``keepdims=True``, ``ndim`` of the output is equal to that of the input.

    >>> jnp.median(x, axis=1, keepdims=True)
    Array([[3. ],
           [4. ],
           [4.5]], dtype=float32)
  """
  check_arraylike("median", a)
  return quantile(a, 0.5, axis=axis, out=out, overwrite_input=overwrite_input,
                  keepdims=keepdims, method='midpoint')
