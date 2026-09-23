def eigh(
    H,
    *,
    precision='float32',
    termination_size=256,
    n=None,
    sort_eigenvalues=True,
    subset_by_index=None,
):
  """Computes the eigendecomposition of the symmetric/Hermitian matrix H.

  Args:
    H: The `n x n` Hermitian input, padded to `N x N`.
    precision: :class:`~jax.lax.Precision` object specifying the matmul
      precision.
    termination_size: Recursion ends once the blocks reach this linear size.
    n: the true (dynamic) size of the matrix.
    sort_eigenvalues: If `True`, the eigenvalues will be sorted from lowest to
      highest.
    subset_by_index: Optional 2-tuple [start, end] indicating the range of
      indices of eigenvalues to compute. For example, is ``range_select`` =
      [n-2,n], then ``eigh`` computes the two largest eigenvalues and their
      eigenvectors.

  Returns:
    vals: The `n` eigenvalues of `H`.
    vecs: A unitary matrix such that `vecs[:, i]` is a normalized eigenvector
      of `H` corresponding to `vals[i]`. We have `H @ vecs = vals * vecs` up
      to numerical error.
  """
  M, N = H.shape
  if M != N:
    raise TypeError(f"Input H of shape {H.shape} must be square.")
  if n is not None and n > N:
    raise ValueError('Static size must be greater or equal to dynamic size.')

  compute_slice = False
  if not subset_by_index is None:
    compute_slice = subset_by_index != (0, n)
    if len(subset_by_index) != 2:
      raise ValueError('subset_by_index must be a tuple of size 2.')
    if subset_by_index[0] >= subset_by_index[1]:
      raise ValueError('Got empty index range in subset_by_index.')
    if subset_by_index[0] < 0:
      raise ValueError('Indices in subset_by_index must be non-negative.')
    range_max = N if n is None else n
    if subset_by_index[1] > range_max:
      raise ValueError('Index in subset_by_index[1] exceeds matrix size.')

  if N <= termination_size:
    if n is not None:
      H = _mask(H, (n, n))
    eig_vals, eig_vecs = lax_linalg.eigh_jacobi(
        H, sort_eigenvalues=(sort_eigenvalues or compute_slice)
    )
    if compute_slice:
      eig_vals = eig_vals[subset_by_index[0] : subset_by_index[1]]
      eig_vecs = eig_vecs[:, subset_by_index[0] : subset_by_index[1]]

  n = N if n is None else n
  with jax.default_matmul_precision(precision):
    eig_vals, eig_vecs = _eigh_work(
        H, n, termination_size=termination_size, subset_by_index=subset_by_index
    )
  eig_vals = _mask(ufuncs.real(eig_vals), (n,), jnp.nan)
  if sort_eigenvalues or compute_slice:
    sort_idxs = jnp.argsort(eig_vals)
    if compute_slice:
      sort_idxs = sort_idxs[subset_by_index[0] : subset_by_index[1]]
    eig_vals = eig_vals[sort_idxs]
    eig_vecs = eig_vecs[:, sort_idxs]

  return eig_vals, eig_vecs
