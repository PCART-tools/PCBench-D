@partial(
    jit,
    static_argnames=(
        "full_matrices",
        "compute_uv",
        "hermitian",
        "subset_by_index",
    ),
)
def svd(
    a: ArrayLike,
    full_matrices: bool = True,
    compute_uv: bool = True,
    hermitian: bool = False,
    subset_by_index: tuple[int, int] | None = None,
) -> Array | SVDResult:
  r"""Compute the singular value decomposition.

  JAX implementation of :func:`numpy.linalg.svd`, implemented in terms of
  :func:`jax.lax.linalg.svd`.

  The SVD of a matrix `A` is given by

  .. math::

     A = U\Sigma V^H

  - :math:`U` contains the left singular vectors and satisfies :math:`U^HU=I`
  - :math:`V` contains the right singular vectors and satisfies :math:`V^HV=I`
  - :math:`\Sigma` is a diagonal matrix of singular values.

  Args:
    a: input array, of shape ``(..., N, M)``
    full_matrices: if True (default) compute the full matrices; i.e. ``u`` and ``vh`` have
      shape ``(..., N, N)`` and ``(..., M, M)``. If False, then the shapes are
      ``(..., N, K)`` and ``(..., K, M)`` with ``K = min(N, M)``.
    compute_uv: if True (default), return the full SVD ``(u, s, vh)``. If False then return
      only the singular values ``s``.
    hermitian: if True, assume the matrix is hermitian, which allows for a more efficient
      implementation (default=False)
    subset_by_index: (TPU-only) Optional 2-tuple [start, end] indicating the range of
      indices of singular values to compute. For example, if ``[n-2, n]`` then
      ``svd`` computes the two largest singular values and their singular vectors.
      Only compatible with ``full_matrices=False``.

  Returns:
    A tuple of arrays ``(u, s, vh)`` if ``compute_uv`` is True, otherwise the array ``s``.

    - ``u``: left singular vectors of shape ``(..., N, N)`` if ``full_matrices`` is True
      or ``(..., N, K)`` otherwise.
    - ``s``: singular values of shape ``(..., K)``
    - ``vh``: conjugate-transposed right singular vectors of shape ``(..., M, M)``
      if ``full_matrices`` is True or ``(..., K, M)`` otherwise.

    where ``K = min(N, M)``.

  See also:
    - :func:`jax.scipy.linalg.svd`: SciPy-style SVD API
    - :func:`jax.lax.linalg.svd`: XLA-style SVD API

  Examples:
    Consider the SVD of a small real-valued array:

    >>> x = jnp.array([[1., 2., 3.],
    ...                [6., 5., 4.]])
    >>> u, s, vt = jnp.linalg.svd(x, full_matrices=False)
    >>> s  # doctest: +SKIP
    Array([9.361919 , 1.8315067], dtype=float32)

    The singular vectors are in the columns of ``u`` and ``v = vt.T``. These vectors are
    orthonormal, which can be demonstrated by comparing the matrix product with the
    identity matrix:

    >>> jnp.allclose(u.T @ u, jnp.eye(2), atol=1E-5)
    Array(True, dtype=bool)
    >>> v = vt.T
    >>> jnp.allclose(v.T @ v, jnp.eye(2), atol=1E-5)
    Array(True, dtype=bool)

    Given the SVD, ``x`` can be reconstructed via matrix multiplication:

    >>> x_reconstructed = u @ jnp.diag(s) @ vt
    >>> jnp.allclose(x_reconstructed, x)
    Array(True, dtype=bool)
  """
  check_arraylike("jnp.linalg.svd", a)
  a, = promote_dtypes_inexact(jnp.asarray(a))
  if hermitian:
    w, v = lax_linalg.eigh(a, subset_by_index=subset_by_index)
    s = lax.abs(v)
    if compute_uv:
      sign = lax.sign(v)
      idxs = lax.broadcasted_iota(np.int64, s.shape, dimension=s.ndim - 1)
      s, idxs, sign = lax.sort((s, idxs, sign), dimension=-1, num_keys=1)
      s = lax.rev(s, dimensions=[s.ndim - 1])
      idxs = lax.rev(idxs, dimensions=[s.ndim - 1])
      sign = lax.rev(sign, dimensions=[s.ndim - 1])
      u = jnp.take_along_axis(w, idxs[..., None, :], axis=-1)
      vh = _H(u * sign[..., None, :].astype(u.dtype))
      return SVDResult(u, s, vh)
    else:
      return lax.rev(lax.sort(s, dimension=-1), dimensions=[s.ndim-1])

  if compute_uv:
    u, s, vh = lax_linalg.svd(
        a,
        full_matrices=full_matrices,
        compute_uv=True,
        subset_by_index=subset_by_index,
    )
    return SVDResult(u, s, vh)
  else:
    return lax_linalg.svd(
        a,
        full_matrices=full_matrices,
        compute_uv=False,
        subset_by_index=subset_by_index,
    )
