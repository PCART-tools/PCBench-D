def cross(x1: ArrayLike, x2: ArrayLike, /, *, axis=-1):
  r"""Compute the cross-product of two 3D vectors

  JAX implementation of :func:`numpy.linalg.cross`

  Args:
    x1: N-dimensional array, with ``x1.shape[axis] == 3``
    x2: N-dimensional array, with ``x2.shape[axis] == 3``, and other axes
      broadcast-compatible with ``x1``.
    axis: axis along which to take the cross product (default: -1).

  Returns:
    array containing the result of the cross-product

  See Also:
    :func:`jax.numpy.cross`: more flexible cross-product API.

  Examples:

    Showing that :math:`\hat{x} \times \hat{y} = \hat{z}`:

    >>> x = jnp.array([1., 0., 0.])
    >>> y = jnp.array([0., 1., 0.])
    >>> jnp.linalg.cross(x, y)
    Array([0., 0., 1.], dtype=float32)

    Cross product of :math:`\hat{x}` with all three standard unit vectors,
    via broadcasting:

    >>> xyz = jnp.eye(3)
    >>> jnp.linalg.cross(x, xyz, axis=-1)
    Array([[ 0.,  0.,  0.],
           [ 0.,  0.,  1.],
           [ 0., -1.,  0.]], dtype=float32)
  """
  check_arraylike("jnp.linalg.outer", x1, x2)
  x1, x2 = jnp.asarray(x1), jnp.asarray(x2)
  if x1.shape[axis] != 3 or x2.shape[axis] != 3:
    raise ValueError(
        "Both input arrays must be (arrays of) 3-dimensional vectors, "
        f"but they have {x1.shape[axis]=} and {x2.shape[axis]=}"
    )
  return jnp.cross(x1, x2, axis=axis)
