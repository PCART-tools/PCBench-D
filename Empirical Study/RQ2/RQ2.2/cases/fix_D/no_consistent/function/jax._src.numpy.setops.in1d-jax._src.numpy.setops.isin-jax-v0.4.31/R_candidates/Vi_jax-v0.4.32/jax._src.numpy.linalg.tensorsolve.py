def tensorsolve(a: ArrayLike, b: ArrayLike, axes: tuple[int, ...] | None = None) -> Array:
  """Solve the tensor equation a x = b for x.

  JAX implementation of :func:`numpy.linalg.tensorsolve`.

  Args:
    a: input array. After reordering via ``axes`` (see below), shape must be
      ``(*b.shape, *x.shape)``.
    b: right-hand-side array.
    axes: optional tuple specifying axes of ``a`` that should be moved to the end

  Returns:
    array x such that after reordering of axes of ``a``, ``tensordot(a, x, x.ndim)``
    is equivalent to ``b``.

  See also:
    - :func:`jax.numpy.linalg.tensordot`
    - :func:`jax.numpy.linalg.tensorinv`

  Examples:
    >>> key1, key2 = jax.random.split(jax.random.key(8675309))
    >>> a = jax.random.normal(key1, shape=(2, 2, 4))
    >>> b = jax.random.normal(key2, shape=(2, 2))
    >>> x = jnp.linalg.tensorsolve(a, b)
    >>> x.shape
    (4,)

    Now show that ``x`` can be used to reconstruct ``b`` using
    :func:`~jax.numpy.linalg.tensordot`:

    >>> b_reconstructed = jnp.linalg.tensordot(a, x, axes=x.ndim)
    >>> jnp.allclose(b, b_reconstructed)
    Array(True, dtype=bool)
  """
  check_arraylike("tensorsolve", a, b)
  a_arr, b_arr = jnp.asarray(a), jnp.asarray(b)
  if axes is not None:
    a_arr = jnp.moveaxis(a_arr, axes, len(axes) * (a_arr.ndim - 1,))
  out_shape = a_arr.shape[b_arr.ndim:]
  if a_arr.shape[:b_arr.ndim] != b_arr.shape:
    raise ValueError("After moving axes to end, leading shape of a must match shape of b."
                     f" got a.shape={a_arr.shape}, b.shape={b_arr.shape}")
  if b_arr.size != math.prod(out_shape):
    raise ValueError("Input arrays must have prod(a.shape[:b.ndim]) == prod(a.shape[b.ndim:]);"
                     f" got a.shape={a_arr.shape}, b.ndim={b_arr.ndim}.")
  a_arr = a_arr.reshape(b_arr.size, math.prod(out_shape))
  return solve(a_arr, b_arr.ravel()).reshape(out_shape)
