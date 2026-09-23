def eye(N: DimSize, M: DimSize | None = None,
        k: int | ArrayLike = 0,
        dtype: DTypeLike | None = None,
        *, device: xc.Device | Sharding | None = None) -> Array:
  """Create a square or rectangular identity matrix

  JAX implementation of :func:`numpy.eye`.

  Args:
    N: integer specifying the first dimension of the array.
    M: optional integer specifying the second dimension of the array;
      defaults to the same value as ``N``.
    k: optional integer specifying the offset of the diagonal. Use positive
      values for upper diagonals, and negative values for lower diagonals.
      Default is zero.
    dtype: optional dtype; defaults to floating point.
    device: optional :class:`~jax.Device` or :class:`~jax.sharding.Sharding`
      to which the created array will be committed.

  Returns:
    Identity array of shape ``(N, M)``, or ``(N, N)`` if ``M`` is not specified.

  See also:
    :func:`jax.numpy.identity`: Simpler API for generating square identity matrices.

  Examples:
    A simple 3x3 identity matrix:

    >>> jnp.eye(3)
    Array([[1., 0., 0.],
           [0., 1., 0.],
           [0., 0., 1.]], dtype=float32)

    Integer identity matrices with offset diagonals:

    >>> jnp.eye(3, k=1, dtype=int)
    Array([[0, 1, 0],
           [0, 0, 1],
           [0, 0, 0]], dtype=int32)
    >>> jnp.eye(3, k=-1, dtype=int)
    Array([[0, 0, 0],
           [1, 0, 0],
           [0, 1, 0]], dtype=int32)

    Non-square identity matrix:

    >>> jnp.eye(3, 5, k=1)
    Array([[0., 1., 0., 0., 0.],
           [0., 0., 1., 0., 0.],
           [0., 0., 0., 1., 0.]], dtype=float32)
  """
  # TODO(vfdev-5): optimize putting the array directly on the device specified
  # instead of putting it on default device and then on the specific device
  output = _eye(N, M=M, k=k, dtype=dtype)
  if device is not None:
    return jax.device_put(output, device=device)
  return output
