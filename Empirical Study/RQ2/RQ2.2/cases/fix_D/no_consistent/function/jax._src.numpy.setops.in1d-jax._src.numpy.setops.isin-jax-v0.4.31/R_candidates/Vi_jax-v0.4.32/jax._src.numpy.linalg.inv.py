@jit
def inv(a: ArrayLike) -> Array:
  """Return the inverse of a square matrix

  JAX implementation of :func:`numpy.linalg.inv`.

  Args:
    a: array of shape ``(..., N, N)`` specifying square array(s) to be inverted.

  Returns:
    Array of shape ``(..., N, N)`` containing the inverse of the input.

  Notes:
    In most cases, explicitly computing the inverse of a matrix is ill-advised. For
    example, to compute ``x = inv(A) @ b``, it is more performant and numerically
    precise to use a direct solve, such as :func:`jax.scipy.linalg.solve`.

  See Also:
    - :func:`jax.scipy.linalg.inv`: SciPy-style API for matrix inverse
    - :func:`jax.numpy.linalg.solve`: direct linear solver

  Examples:
    Compute the inverse of a 3x3 matrix

    >>> a = jnp.array([[1., 2., 3.],
    ...                [2., 4., 2.],
    ...                [3., 2., 1.]])
    >>> a_inv = jnp.linalg.inv(a)
    >>> a_inv  # doctest: +SKIP
    Array([[ 0.        , -0.25      ,  0.5       ],
           [-0.25      ,  0.5       , -0.25000003],
           [ 0.5       , -0.25      ,  0.        ]], dtype=float32)

    Check that multiplying with the inverse gives the identity:

    >>> jnp.allclose(a @ a_inv, jnp.eye(3), atol=1E-5)
    Array(True, dtype=bool)

    Multiply the inverse by a vector ``b``, to find a solution to ``a @ x = b``

    >>> b = jnp.array([1., 4., 2.])
    >>> a_inv @ b
    Array([ 0.  ,  1.25, -0.5 ], dtype=float32)

    Note, however, that explicitly computing the inverse in such a case can lead
    to poor performance and loss of precision as the size of the problem grows.
    Instead, you should use a direct solver like :func:`jax.numpy.linalg.solve`:

    >>> jnp.linalg.solve(a, b)
     Array([ 0.  ,  1.25, -0.5 ], dtype=float32)
  """
  check_arraylike("jnp.linalg.inv", a)
  arr = jnp.asarray(a)
  if arr.ndim < 2 or arr.shape[-1] != arr.shape[-2]:
    raise ValueError(
      f"Argument to inv must have shape [..., n, n], got {arr.shape}.")
  return solve(
    arr, lax.broadcast(jnp.eye(arr.shape[-1], dtype=arr.dtype), arr.shape[:-2]))
