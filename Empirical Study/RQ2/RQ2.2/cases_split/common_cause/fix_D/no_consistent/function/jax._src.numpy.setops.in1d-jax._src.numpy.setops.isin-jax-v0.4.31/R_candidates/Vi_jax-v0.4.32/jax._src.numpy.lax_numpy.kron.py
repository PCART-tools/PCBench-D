@jit
def kron(a: ArrayLike, b: ArrayLike) -> Array:
  """Compute the Kronecker product of two input arrays.

  JAX implementation of :func:`numpy.kron`.

  The Kronecker product is an operation on two matrices of arbitrary size that
  produces a block matrix. Each element of the first matrix ``a`` is multiplied by
  the entire second matrix ``b``. If ``a`` has shape (m, n) and ``b``
  has shape (p, q), the resulting matrix will have shape (m * p, n * q).

  Args:
    a: first input array with any shape.
    b: second input array with any shape.

  Returns:
    A new array representing the Kronecker product of the inputs  ``a`` and ``b``.
    The shape of the output is the element-wise product of the input shapes.

  See also:
    - :func:`jax.numpy.outer`: compute the outer product of two arrays.

  Examples:
    >>> a = jnp.array([[1, 2],
    ...                [3, 4]])
    >>> b = jnp.array([[5, 6],
    ...                [7, 8]])
    >>> jnp.kron(a, b)
    Array([[ 5,  6, 10, 12],
           [ 7,  8, 14, 16],
           [15, 18, 20, 24],
           [21, 24, 28, 32]], dtype=int32)
  """
  util.check_arraylike("kron", a, b)
  a, b = util.promote_dtypes(a, b)
  if ndim(a) < ndim(b):
    a = expand_dims(a, range(ndim(b) - ndim(a)))
  elif ndim(b) < ndim(a):
    b = expand_dims(b, range(ndim(a) - ndim(b)))
  a_reshaped = expand_dims(a, range(1, 2 * ndim(a), 2))
  b_reshaped = expand_dims(b, range(0, 2 * ndim(b), 2))
  out_shape = tuple(np.multiply(shape(a), shape(b)))
  return reshape(lax.mul(a_reshaped, b_reshaped), out_shape)
