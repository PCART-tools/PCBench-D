@partial(jit, inline=True)
def minimum(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise minimum of the input arrays.

  JAX implementation of :obj:`numpy.minimum`.

  Args:
    x: input array or scalar.
    y: input array or scalar. Both ``x`` and ``y`` should either have same shape
      or be broadcast compatible.

  Returns:
    An array containing the element-wise minimum of ``x`` and ``y``.

  Note:
    For each pair of elements, ``jnp.minimum`` returns:
      - smaller of the two if both elements are finite numbers.
      - ``nan`` if one element is ``nan``.

  See also:
    - :func:`jax.numpy.maximum`: Returns element-wise maximum of the input arrays.
    - :func:`jax.numpy.fmin`: Returns element-wise minimum of the input arrays,
      ignoring NaNs.
    - :func:`jax.numpy.amin`: Returns the minimum of array elements along a given
      axis.
    - :func:`jax.numpy.nanmin`: Returns the minimum of the array elements along
      a given axis, ignoring NaNs.

  Examples:
    Inputs with ``x.shape == y.shape``:

    >>> x = jnp.array([2, 3, 5, 1])
    >>> y = jnp.array([-3, 6, -4, 7])
    >>> jnp.minimum(x, y)
    Array([-3,  3, -4,  1], dtype=int32)

    Inputs having broadcast compatibility:

    >>> x1 = jnp.array([[1, 5, 2],
    ...                 [-3, 4, 7]])
    >>> y1 = jnp.array([-2, 3, 6])
    >>> jnp.minimum(x1, y1)
    Array([[-2,  3,  2],
           [-3,  3,  6]], dtype=int32)

    Inputs with ``nan``:

    >>> nan = jnp.nan
    >>> x2 = jnp.array([[2.5, nan, -2],
    ...                 [nan, 5, 6],
    ...                 [-4, 3, 7]])
    >>> y2 = jnp.array([1, nan, 5])
    >>> jnp.minimum(x2, y2)
    Array([[ 1., nan, -2.],
           [nan, nan,  5.],
           [-4., nan,  5.]], dtype=float32)
  """
  return lax.min(*promote_args("minimum", x, y))
