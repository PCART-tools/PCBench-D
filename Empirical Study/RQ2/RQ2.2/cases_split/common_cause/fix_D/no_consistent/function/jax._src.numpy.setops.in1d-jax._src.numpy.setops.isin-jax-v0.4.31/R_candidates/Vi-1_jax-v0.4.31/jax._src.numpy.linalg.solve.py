@jit
def solve(a: ArrayLike, b: ArrayLike) -> Array:
  """Solve a linear system of equations

  JAX implementation of :func:`numpy.linalg.solve`.

  This solves a (batched) linear system of equations ``a @ x = b``
  for ``x`` given ``a`` and ``b``.

  Args:
    a: array of shape ``(..., N, N)``.
    b: array of shape ``(N,)`` (for 1-dimensional right-hand-side) or
      ``(..., N, M)`` (for batched 2-dimensional right-hand-side).

  Returns:
    An array containing the result of the linear solve. The result has shape ``(..., N)``
    if ``b`` is of shape ``(N,)``, and has shape ``(..., N, M)`` otherwise.

  See also:
    - :func:`jax.scipy.linalg.solve`: SciPy-style API for solving linear systems.
    - :func:`jax.lax.custom_linear_solve`: matrix-free linear solver.

  Examples:
    A simple 3x3 linear system:

    >>> A = jnp.array([[1., 2., 3.],
    ...                [2., 4., 2.],
    ...                [3., 2., 1.]])
    >>> b = jnp.array([14., 16., 10.])
    >>> x = jnp.linalg.solve(A, b)
    >>> x
    Array([1., 2., 3.], dtype=float32)

    Confirming that the result solves the system:

    >>> jnp.allclose(A @ x, b)
    Array(True, dtype=bool)
  """
  check_arraylike("jnp.linalg.solve", a, b)
  a, b = promote_dtypes_inexact(jnp.asarray(a), jnp.asarray(b))

  if b.ndim == 1:
    signature = "(m,m),(m)->(m)"
  elif a.ndim == b.ndim + 1:
    # Deprecation warning added 2024-02-06
    warnings.warn("jnp.linalg.solve: batched 1D solves with b.ndim > 1 are deprecated, "
                  "and in the future will be treated as a batched 2D solve. "
                  "Use solve(a, b[..., None])[..., 0] to avoid this warning.",
                  category=FutureWarning)
    signature = "(m,m),(m)->(m)"
  else:
    signature = "(m,m),(m,n)->(m,n)"
  return jnp.vectorize(lax_linalg._solve, signature=signature)(a, b)
