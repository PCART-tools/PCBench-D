@partial(jit, static_argnames=['upper'])
def cholesky(a: ArrayLike, *, upper: bool = False) -> Array:
  """Compute the Cholesky decomposition of a matrix.

  JAX implementation of :func:`numpy.linalg.cholesky`.

  The Cholesky decomposition of a matrix `A` is:

  .. math::

     A = U^HU

  or

  .. math::

    A = LL^H

  where `U` is an upper-triangular matrix and `L` is a lower-triangular matrix, and
  :math:`X^H` is the Hermitian transpose of `X`.

  Args:
    a: input array, representing a (batched) positive-definite hermitian matrix.
      Must have shape ``(..., N, N)``.
    upper: if True, compute the upper Cholesky decomposition `L`. if False
      (default), compute the lower Cholesky decomposition `U`.

  Returns:
    array of shape ``(..., N, N)`` representing the Cholesky decomposition
    of the input. If the input is not Hermitian positive-definite, The result
    will contain NaN entries.


  See also:
    - :func:`jax.scipy.linalg.cholesky`: SciPy-style Cholesky API
    - :func:`jax.lax.linalg.cholesky`: XLA-style Cholesky API

  Examples:
    A small real Hermitian positive-definite matrix:

    >>> x = jnp.array([[2., 1.],
    ...                [1., 2.]])

    Lower Cholesky factorization:

    >>> jnp.linalg.cholesky(x)
    Array([[1.4142135 , 0.        ],
           [0.70710677, 1.2247449 ]], dtype=float32)

    Upper Cholesky factorization:

    >>> jnp.linalg.cholesky(x, upper=True)
    Array([[1.4142135 , 0.70710677],
           [0.        , 1.2247449 ]], dtype=float32)

    Reconstructing ``x`` from its factorization:

    >>> L = jnp.linalg.cholesky(x)
    >>> jnp.allclose(x, L @ L.T)
    Array(True, dtype=bool)
  """
  check_arraylike("jnp.linalg.cholesky", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  L = lax_linalg.cholesky(a)
  return L.mT.conj() if upper else L
