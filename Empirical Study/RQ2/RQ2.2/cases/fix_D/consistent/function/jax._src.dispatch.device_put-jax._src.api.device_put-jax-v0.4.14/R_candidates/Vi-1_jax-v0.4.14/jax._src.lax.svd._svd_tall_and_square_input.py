@functools.partial(jax.jit, static_argnums=(1, 2, 3))
def _svd_tall_and_square_input(
    a: Any, hermitian: bool, compute_uv: bool, max_iterations: int
) -> Union[Any, Sequence[Any]]:
  """Singular value decomposition for m x n matrix and m >= n.

  Args:
    a: A matrix of shape `m x n` with `m >= n`.
    hermitian: True if `a` is Hermitian.
    compute_uv: Whether to compute also `u` and `v` in addition to `s`.
    max_iterations: The predefined maximum number of iterations of QDWH.

  Returns:
    A 3-tuple (`u`, `s`, `v`), where `u` is a unitary matrix of shape `m x n`,
    `s` is vector of length `n` containing the singular values in the descending
    order, `v` is a unitary matrix of shape `n x n`, and
    `a = (u * s) @ v.T.conj()`. For `compute_uv=False`, only `s` is returned.
  """

  u, h, _, _ = lax.linalg.qdwh(a, is_hermitian=hermitian,
                               max_iterations=max_iterations)

  # TODO: Uses `eigvals_only=True` if `compute_uv=False`.
  v, s = lax.linalg.eigh(h)
  # Singular values are non-negative by definition. But eigh could return small
  # negative values, so we clamp them to zero.
  s = jnp.maximum(s, 0.0)

  # Flips the singular values in descending order.
  s_out = jnp.flip(s)

  if not compute_uv:
    return s_out

  # Reorders eigenvectors.
  v_out = jnp.fliplr(v)

  u_out = u @ v_out

  # Makes correction if computed `u` from qdwh is not unitary.
  # Section 5.5 of Nakatsukasa, Yuji, and Nicholas J. Higham. "Stable and
  # efficient spectral divide and conquer algorithms for the symmetric
  # eigenvalue decomposition and the SVD." SIAM Journal on Scientific Computing
  # 35, no. 3 (2013): A1325-A1349.
  def correct_rank_deficiency(u_out):
    u_out, r = lax.linalg.qr(u_out, full_matrices=False)
    u_out = u_out @ jnp.diag(lax.sign(jnp.diag(r)))
    return u_out

  eps = float(jnp.finfo(a.dtype).eps)
  u_out = lax.cond(s[0] < a.shape[1] * eps * s_out[0],
                   correct_rank_deficiency,
                   lambda u_out: u_out,
                   operand=(u_out))

  return (u_out, s_out, v_out)
