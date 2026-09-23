def eig_jvp_rule(primals, tangents, *, compute_left_eigenvectors,
                 compute_right_eigenvectors):
  if compute_left_eigenvectors or compute_right_eigenvectors:
    raise NotImplementedError(
        'The derivatives of eigenvectors are not implemented, only '
        'eigenvalues. See '
        'https://github.com/google/jax/issues/2748 for discussion.')
  # Formula for derivative of eigenvalues w.r.t. a is eqn 4.60 in
  # https://arxiv.org/abs/1701.00392
  a, = primals
  da, = tangents
  l, v = eig(a, compute_left_eigenvectors=False)
  return [l], [reductions.sum(_solve(v, da.astype(v.dtype)) * _T(v), -1)]
