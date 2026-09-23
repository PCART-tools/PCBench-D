def split_spectrum(H, n, split_point, V0=None):
  """ The Hermitian matrix `H` is split into two matrices `H_minus`
  `H_plus`, respectively sharing its eigenspaces beneath and above
  its `split_point`th eigenvalue.

  Returns, in addition, `V_minus` and `V_plus`, isometries such that
  `Hi = Vi.conj().T @ H @ Vi`. If `V0` is not None, `V0 @ Vi` are
  returned instead; this allows the overall isometries mapping from
  an initial input matrix to progressively smaller blocks to be formed.

  Args:
    H: The Hermitian matrix to split.
    split_point: The eigenvalue to split along.
    V0: Matrix of isometries to be updated.
  Returns:
    H_minus: A Hermitian matrix sharing the eigenvalues of `H` beneath
      `split_point`.
    V_minus: An isometry from the input space of `V0` to `H_minus`.
    H_plus: A Hermitian matrix sharing the eigenvalues of `H` above
      `split_point`.
    V_plus: An isometry from the input space of `V0` to `H_plus`.
    rank: The dynamic size of the m subblock.
  """
  N, _ = H.shape
  H_shift = H - (split_point * jnp.eye(N, dtype=split_point.dtype)).astype(H.dtype)
  U, _, _, _ = qdwh.qdwh(H_shift, is_hermitian=True, dynamic_shape=(n, n))
  P = -0.5 * (U - _mask(jnp.eye(N, dtype=H.dtype), (n, n)))
  rank = jnp.round(jnp.trace(jnp.real(P))).astype(jnp.int32)

  V_minus, V_plus = _projector_subspace(P, H, n, rank)
  H_minus = (V_minus.conj().T @ H) @ V_minus
  H_plus = (V_plus.conj().T @ H) @ V_plus
  if V0 is not None:
    V_minus = jnp.dot(V0, V_minus)
    V_plus = jnp.dot(V0, V_plus)
  return H_minus, V_minus, H_plus, V_plus, rank
