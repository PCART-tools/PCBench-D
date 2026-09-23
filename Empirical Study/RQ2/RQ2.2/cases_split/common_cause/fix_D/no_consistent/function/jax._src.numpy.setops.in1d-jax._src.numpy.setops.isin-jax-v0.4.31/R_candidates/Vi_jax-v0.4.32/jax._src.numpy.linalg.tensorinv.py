def tensorinv(a: ArrayLike, ind: int = 2) -> Array:
  """Compute the tensor inverse of an array.

  JAX implementation of :func:`numpy.linalg.tensorinv`.

  This computes the inverse of the :func:`~jax.numpy.linalg.tensordot`
  operation with the same ``ind`` value.

  Args:
    a: array to be inverted. Must have ``prod(a.shape[:ind]) == prod(a.shape[ind:])``
    ind: positive integer specifying the number of indices in the tensor product.

  Returns:
    array of shape ``(*a.shape[ind:], *a.shape[:ind])`` containing the
    tensor inverse of ``a``.

  See also:
    - :func:`jax.numpy.linalg.tensordot`
    - :func:`jax.numpy.linalg.tensorsolve`

  Examples:
    >>> key = jax.random.key(1337)
    >>> x = jax.random.normal(key, shape=(2, 2, 4))
    >>> xinv = jnp.linalg.tensorinv(x, 2)
    >>> xinv_x = jnp.linalg.tensordot(xinv, x, axes=2)
    >>> jnp.allclose(xinv_x, jnp.eye(4), atol=1E-4)
    Array(True, dtype=bool)
  """
  check_arraylike("tensorinv", a)
  arr = jnp.asarray(a)
  ind = operator.index(ind)
  if ind <= 0:
    raise ValueError(f"ind must be a positive integer; got {ind=}")
  contracting_shape, batch_shape = arr.shape[:ind], arr.shape[ind:]
  flatshape = (math.prod(contracting_shape), math.prod(batch_shape))
  if flatshape[0] != flatshape[1]:
    raise ValueError("tensorinv is only possible when the product of the first"
                     " `ind` dimensions equals that of the remaining dimensions."
                     f" got {arr.shape=} with {ind=}.")
  return inv(arr.reshape(flatshape)).reshape(*batch_shape, *contracting_shape)
