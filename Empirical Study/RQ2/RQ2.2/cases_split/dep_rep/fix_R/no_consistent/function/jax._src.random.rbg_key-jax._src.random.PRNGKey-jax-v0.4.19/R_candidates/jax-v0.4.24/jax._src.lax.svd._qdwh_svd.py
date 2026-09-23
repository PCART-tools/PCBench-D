@functools.partial(jax.jit, static_argnums=(1, 2, 3, 4))
def _qdwh_svd(a: Any,
              full_matrices: bool,
              compute_uv: bool = True,
              hermitian: bool = False,
              max_iterations: int = 10) -> Any | Sequence[Any]:
  """Singular value decomposition.

  Args:
    a: A matrix of shape `m x n`.
    full_matrices: If True, `u` and `vh` have the shapes `m x m` and `n x n`,
      respectively. If False, the shapes are `m x k` and `k x n`, respectively,
      where `k = min(m, n)`.
    compute_uv: Whether to compute also `u` and `v` in addition to `s`.
    hermitian: True if `a` is Hermitian.
    max_iterations: The predefined maximum number of iterations of QDWH.

  Returns:
    A 3-tuple (`u`, `s`, `vh`), where `u` and `vh` are unitary matrices,
    `s` is vector of length `k` containing the singular values in the
    non-increasing order, and `k = min(m, n)`. The shapes of `u` and `vh`
    depend on the value of `full_matrices`. For `compute_uv=False`,
    only `s` is returned.
  """
  m, n = a.shape

  is_flip = False
  if m < n:
    a = a.T.conj()
    m, n = a.shape
    is_flip = True

  reduce_to_square = False
  if full_matrices:
    q_full, a_full = lax.linalg.qr(a, full_matrices=True)
    q = q_full[:, :n]
    u_out_null = q_full[:, n:]
    a = a_full[:n, :]
    reduce_to_square = True
  else:
    # The constant `1.15` comes from Yuji Nakatsukasa's implementation
    # https://www.mathworks.com/matlabcentral/fileexchange/36830-symmetric-eigenvalue-decomposition-and-the-svd?s_tid=FX_rc3_behav
    if m > 1.15 * n:
      q, a = lax.linalg.qr(a, full_matrices=False)
      reduce_to_square = True

  if not compute_uv:
    with jax.default_matmul_precision('float32'):
      return _svd_tall_and_square_input(a, hermitian, compute_uv,
                                        max_iterations)

  with jax.default_matmul_precision('float32'):
    u_out, s_out, v_out = _svd_tall_and_square_input(
        a, hermitian, compute_uv, max_iterations)
    if reduce_to_square:
      u_out = q @ u_out

  if full_matrices:
    u_out = jnp.hstack((u_out, u_out_null))

  if is_flip:
    return(v_out, s_out, u_out.T.conj())

  return (u_out, s_out, v_out.T.conj())
