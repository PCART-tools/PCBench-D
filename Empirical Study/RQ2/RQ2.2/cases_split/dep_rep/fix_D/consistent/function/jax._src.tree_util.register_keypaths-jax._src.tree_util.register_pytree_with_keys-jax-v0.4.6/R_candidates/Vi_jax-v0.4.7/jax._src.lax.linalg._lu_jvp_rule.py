def _lu_jvp_rule(primals, tangents):
  a, = primals
  a_dot, = tangents
  lu, pivots, permutation = lu_p.bind(a)

  a_shape = jnp.shape(a)
  m, n = a_shape[-2:]
  dtype = lax.dtype(a)
  k = min(m, n)

  batch_dims = a_shape[:-2]
  iotas = jnp.ix_(*(lax.iota(jnp.int32, b) for b in batch_dims + (1,)))
  x = a_dot[iotas[:-1] + (permutation, slice(None))]

  # Differentiation of Matrix Functionals Using Triangular Factorization
  # F. R. De Hoog, R. S. Anderssen, and M. A. Lukas
  #
  #     LU = A
  # ==> L'U + LU' = A'
  # ==> inv(L) . L' + U' . inv(U) = inv(L) A' inv(U)
  # ==> L' = L . tril(inv(L) . A' . inv(U), -1)
  #     U' = triu(inv(L) . A' . inv(U)) . U

  ndims = len(a_shape)
  l_padding = [(0, 0, 0)] * ndims
  l_padding[-1] = (0, m - k, 0)
  zero = lax_internal._const(lu, 0)
  l = lax.pad(jnp.tril(lu[..., :, :k], -1), zero, l_padding)
  l = l + lax.expand_dims(jnp.eye(m, m, dtype=dtype), range(l.ndim - 2))

  u_eye = lax.pad(jnp.eye(n - k, n - k, dtype=dtype), zero,
                  ((k, 0, 0), (k, 0, 0)))
  u_padding = [(0, 0, 0)] * ndims
  u_padding[-2] = (0, n - k, 0)
  u = (lax.pad(jnp.triu(lu[..., :k, :]), zero, u_padding) +
       lax.expand_dims(u_eye, range(lu.ndim - 2)))

  la = triangular_solve(l, x, left_side=True, transpose_a=False, lower=True,
                        unit_diagonal=True)
  lau = triangular_solve(u, la, left_side=False, transpose_a=False,
                         lower=False)

  l_dot = jnp.matmul(l, jnp.tril(lau, -1), precision=lax.Precision.HIGHEST)
  u_dot = jnp.matmul(jnp.triu(lau), u, precision=lax.Precision.HIGHEST)
  lu_dot = l_dot + u_dot
  return (lu, pivots, permutation), (lu_dot, ad_util.Zero.from_value(pivots),
                                     ad_util.Zero.from_value(permutation))
