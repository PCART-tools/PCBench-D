def eigh(H, *, precision="float32", termination_size=256, n=None,
         sort_eigenvalues=True):
  """ Computes the eigendecomposition of the symmetric/Hermitian matrix H.

  Args:
    H: The `n x n` Hermitian input, padded to `N x N`.
    precision: :class:`~jax.lax.Precision` object specifying the matmul precision.
    termination_size: Recursion ends once the blocks reach this linear size.
    n: the true (dynamic) size of the matrix.
    sort_eigenvalues: If `True`, the eigenvalues will be sorted from lowest to
      highest.
  Returns:
    vals: The `n` eigenvalues of `H`.
    vecs: A unitary matrix such that `vecs[:, i]` is a normalized eigenvector
      of `H` corresponding to `vals[i]`. We have `H @ vecs = vals * vecs` up
      to numerical error.
  """
  M, N = H.shape
  if M != N:
    raise TypeError(f"Input H of shape {H.shape} must be square.")

  if N <= termination_size:
    if n is not None:
      H = _mask(H, (n, n), jnp.eye(N, dtype=H.dtype))
    return lax_linalg.eigh_jacobi(
        H, sort_eigenvalues=sort_eigenvalues)

  # TODO(phawkins): consider rounding N up to a larger size to maximize reuse
  # between matrices.

  n = N if n is None else n
  with jax.default_matmul_precision(precision):
    eig_vals, eig_vecs = _eigh_work(H, n, termination_size=termination_size)
  eig_vals = _mask(jnp.real(eig_vals), (n,), jnp.nan)
  if sort_eigenvalues:
    sort_idxs = jnp.argsort(eig_vals)
    eig_vals = eig_vals[sort_idxs]
    eig_vecs = eig_vecs[:, sort_idxs]
  return eig_vals, eig_vecs
