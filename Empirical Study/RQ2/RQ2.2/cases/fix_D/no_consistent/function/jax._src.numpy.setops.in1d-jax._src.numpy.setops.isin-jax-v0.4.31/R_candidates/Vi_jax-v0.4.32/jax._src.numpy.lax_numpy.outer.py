@partial(jit, inline=True)
def outer(a: ArrayLike, b: ArrayLike, out: None = None) -> Array:
  """Compute the outer product of two arrays.

  JAX implementation of :func:`numpy.outer`.

  Args:
    a: first input array, if not 1D it will be flattened.
    b: second input array, if not 1D it will be flattened.
    out: unsupported by JAX.

  Returns:
    The outer product of the inputs ``a`` and ``b``. Returned array
    will be of shape ``(a.size, b.size)``.

  See also:
    - :func:`jax.numpy.inner`: compute the inner product of two arrays.
    - :func:`jax.numpy.einsum`: Einstein summation.

  Examples:
    >>> a = jnp.array([1, 2, 3])
    >>> b = jnp.array([4, 5, 6])
    >>> jnp.outer(a, b)
    Array([[ 4,  5,  6],
           [ 8, 10, 12],
           [12, 15, 18]], dtype=int32)
  """
  if out is not None:
    raise NotImplementedError("The 'out' argument to jnp.outer is not supported.")
  util.check_arraylike("outer", a, b)
  a, b = util.promote_dtypes(a, b)
  return ravel(a)[:, None] * ravel(b)[None, :]
