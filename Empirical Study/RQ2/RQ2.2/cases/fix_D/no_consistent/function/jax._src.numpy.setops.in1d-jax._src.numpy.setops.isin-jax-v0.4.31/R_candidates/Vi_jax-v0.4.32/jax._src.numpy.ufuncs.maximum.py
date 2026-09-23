@partial(jit, inline=True)
def maximum(x: ArrayLike, y: ArrayLike, /) -> Array:
  """Return element-wise maximum of the input arrays.

  JAX implementation of :obj:`numpy.maximum`.

  Args:
    x: input array or scalar.
    y: input array or scalar. Both ``x`` and ``y`` should either have same shape
      or be broadcast compatible.

  Returns:
    An array containing the element-wise maximum of ``x`` and ``y``.

  Note:
    For each pair of elements, ``jnp.maximum`` returns:
      - larger of the two if both elements are finite numbers.
      - ``nan`` if one element is ``nan``.

  See also:
    - :func:`jax.numpy.minimum`: Returns element-wise minimum of the input
      arrays.
    - :func:`jax.numpy.fmax`: Returns element-wise maximum of the input arrays,
      ignoring NaNs.
    - :func:`jax.numpy.amax`: Retruns the maximum of array elements along a given
      axis.
    - :func:`jax.numpy.nanmax`: Returns the maximum of the array elements along
      a given axis, ignoring NaNs.

  Examples:
    Inputs with ``x.shape == y.shape``:

    >>> x = jnp.array([1, -5, 3, 2])
    >>> y = jnp.array([-2, 4, 7, -6])
    >>> jnp.maximum(x, y)
    Array([1, 4, 7, 2], dtype=int32)

    Inputs with broadcast compatibility:

    >>> x1 = jnp.array([[-2, 5, 7, 4],
    ...                 [1, -6, 3, 8]])
    >>> y1 = jnp.array([-5, 3, 6, 9])
    >>> jnp.maximum(x1, y1)
    Array([[-2,  5,  7,  9],
           [ 1,  3,  6,  9]], dtype=int32)

    Inputs having ``nan``:

    >>> nan = jnp.nan
    >>> x2 = jnp.array([nan, -3, 9])
    >>> y2 = jnp.array([[4, -2, nan],
    ...                 [-3, -5, 10]])
    >>> jnp.maximum(x2, y2)
    Array([[nan, -2., nan],
          [nan, -3., 10.]], dtype=float32)
  """
  return lax.max(*promote_args("maximum", x, y))
